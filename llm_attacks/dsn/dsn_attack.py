import gc
import traceback
import os
from copy import deepcopy
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from tqdm.auto import tqdm

from llm_attacks import AttackPrompt, MultiPromptAttack, PromptManager
from llm_attacks import get_embedding_matrix, get_embeddings

class UnlikelihoodLoss(nn.Module):
    def __init__(self):
        super(UnlikelihoodLoss, self).__init__()
        self.eps = 0.01

    def forward(self, input, target):
        probabilities = F.softmax(input, dim=1)
        p = probabilities.gather(1, target.unsqueeze(1))
        p = torch.clamp(p, min=0, max=1-self.eps)       # avoid some inf loss case
        loss = -torch.log(1 - p)
        loss = torch.clamp(loss, min=0, max=10)         # avoid some inf loss case
        return loss.squeeze()

def apply_cosine_decay(tensor: torch.Tensor) -> torch.Tensor:
    '''to conduct cosine decay on the last dimension'''
    L = tensor.size(-1)
    decay_weights = 0.5 + 0.5 * torch.cos(torch.linspace(0, 0.5*torch.pi, L, device=tensor.device, dtype=tensor.dtype))
    return tensor * decay_weights

def token_gradients_dsn_loss(model, input_ids, input_slice, target_slice, loss_slice, test_prefixes, test_token_length, test_prefixes_toks, alpha, use_decay=False, use_refusal=False):
    # embedding matrix of [vocab_size, embedding_dim]
    embed_weights = get_embedding_matrix(model)
    # create one-hot matrix of zeros of shape [20,32000]: [length_control, vocab_size]
    one_hot = torch.zeros(
        input_ids[input_slice].shape[0],
        embed_weights.shape[0],
        device=model.device,
        dtype=embed_weights.dtype
    )
    # fill one-hot matrix with current tokens and put 1's at the current token positions
    one_hot.scatter_(
        1,
        input_ids[input_slice].unsqueeze(1),
        torch.ones(one_hot.shape[0], 1, device=model.device, dtype=embed_weights.dtype)
    )
    # enable gradients
    one_hot.requires_grad_()
    # turn token choices into embedding vectors
    # trainable embeddings for control tokens
    input_embeds = (one_hot @ embed_weights).unsqueeze(0)

    # get embeddings of the full input
    embeds = get_embeddings(model, input_ids.unsqueeze(0)).detach()
    # now stitch it together with the rest of the embeddings
    # --> input_embeds replace the original control embeddings with the new trainable ones
    full_embeds = torch.cat(
                        [
                            embeds[:,:input_slice.start,:],
                            input_embeds,
                            embeds[:,input_slice.stop:,:]
                        ],
                        dim=1)

    # run model and get the logits
    logits = model(inputs_embeds=full_embeds).logits
    targets = input_ids[target_slice]

    affirmative_loss = nn.CrossEntropyLoss(reduction='none')(logits[0,loss_slice,:], targets)
    # use_target_loss_cosine_decay=True in DSN
    # so apply cosine decay
    if use_decay:   # cosine decay could only be utlized towards vanilla target loss
        affirmative_loss = apply_cosine_decay(affirmative_loss)
    affirmative_loss = torch.mean(affirmative_loss)

    # DSN case: use_refusal is False
    if not use_refusal: #if no refusal loss
        loss = affirmative_loss
    # else use refusal loss for 
    else:
        refusal_loss = 0
        count_loss = 0
        crit = UnlikelihoodLoss()
        # loop over the refusal phrases
        for j_in_algorithm in range(len(test_prefixes)):
            # get phrase length, e.g. i'm sorry is 2 tokens
            key_word_length = test_token_length[j_in_algorithm]

            # slide over the input --> check every possible position where refusal might appear
            for loss_start in range(loss_slice.start , 99999):
                # stop when window goes past output length
                if loss_start + key_word_length > logits.shape[1]:
                    break
                # select window/slice for the refusal_loss 
                refusal_loss_slice = slice(loss_start, loss_start+key_word_length)
                bs = logits.shape[0]
                # convert target phrase into tensor
                cross_loss_target = torch.tensor(test_prefixes_toks[j_in_algorithm]).unsqueeze(0).to(logits.device)
                # repeat for batch
                cross_loss_target = cross_loss_target.repeat(bs, 1)

                # compute unlikelihoodloss on the refusal loss window; if prob refusal token is high --> high loss
                temp_loss = crit(logits[:,refusal_loss_slice,:].transpose(1,2), cross_loss_target)

                # sum over all windows
                refusal_loss += temp_loss.mean()    # the refusal loss won't utilize cosine decay
                count_loss += 1

        # average refusal loss
        refusal_loss = refusal_loss/count_loss
        # combine the refusal loss with the affirmative loss
        loss = affirmative_loss + alpha * refusal_loss

    # backpropagate
    loss.backward()
    # return gradient tensor
    # --> 20x32000 shape
    # --> for each position in control tokens (row), the values show how good/bad a particular token from the vocab is (columns) 
    return one_hot.grad.clone()

class DSNAttackPrompt(AttackPrompt):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def grad(self, model):
        # use_different_aug_sampling_alpha is set to False in DSN
        if not self.para.use_different_aug_sampling_alpha:
            # in DSN: augmented_loss_alpha=1.0
            sampling_alpha = self.para.augmented_loss_alpha
        else:
            sampling_alpha = self.para.aug_sampling_alpha2
        # use_aug_sampling=False in DSN
        use_refusal = True if self.para.use_aug_sampling else False

        # return gradients 
        return token_gradients_dsn_loss(
            model,
            self.input_ids.to(model.device),
            self._control_slice,
            self._target_slice,
            self._loss_slice,
            self.test_prefixes,
            self.test_token_length,
            self.test_prefixes_toks,
            sampling_alpha,
            use_decay=self.para.use_target_loss_cosine_decay,
            use_refusal=use_refusal
        )

class DSNPromptManager(PromptManager):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def sample_control(self, grad, batch_size, topk=256, temp=1, allow_non_ascii=True):

        # allow_non_ascii=False in DSN
        # do not allow weird tokens
        if not allow_non_ascii:
            grad[:, self._nonascii_toks.to(grad.device)] = np.infty
        # get the indices of the top-k tokens based on the gradient (neg gradient is good)
        # --> so it retrieves best top-k tokens for each position
        top_indices = (-grad).topk(topk, dim=1).indices
        control_toks = self.control_toks.to(grad.device)
        # copy control tokens batchsize times --> [batchsize, control_token_len]
        original_control_toks = control_toks.repeat(batch_size, 1)

        # for each candidate suffix, decide which position to modify
        # new_token_pos has a batchsize number of entries
        # each entry signifies the position in the suffix that ought to be modified
        new_token_pos = torch.arange(
            0,
            len(control_toks),
            len(control_toks) / batch_size,
            device=grad.device
        ).type(torch.int64)

        # for each row/candidate suffix, randomly pick one index inside the top-k list
        # that serves as a replacement token
        new_token_val = torch.gather(
            top_indices[new_token_pos], 1,
            torch.randint(0, topk, (batch_size, 1),
            device=grad.device)
        )
        # print("top indices: ", top_indices)
        # print("topk_nr = ", topk)

        # return the new control candidate tokens, where at position i, the new token value is inserted
        # so for each row/candidate suffix, replace the old token at the specified position with the newly sampled token
        new_control_toks = original_control_toks.scatter_(1, new_token_pos.unsqueeze(-1), new_token_val)

        # return candidate suffixes, where each row is one candidate suffix
        # a candidate suffix only differs from the original suffix in 1 position
        # e.g one token id at one position is replaced with another in the original suffix
        return new_control_toks
    

    # def sample_control(self, grad, batch_size, topk=256, temp=1, allow_non_ascii=True):
    #     '''sample_control function obtained from MAGIC, which is proposed by Li et al. (2024)'''

    #     if not allow_non_ascii:
    #         grad[:, self._nonascii_toks.to(grad.device)] = np.infty

    #     # positions in the control suffix that should be modified
    #     now_grad = []
    #     # loop through all the control tokens
    #     for idx in range(len(self.control_toks)):
    #         # obtain the gradient of the current control token
    #         temp = grad[idx][self.control_toks[idx]]
    #         # only obtain indices of the control suffix that have a positive token gradient 
    #         if temp>0: now_grad.append(idx)

    #     # calculate the number of coordinates/indices that should be modified/updated
    #     now_size = int(len(now_grad)**0.5)

    #     # print(now_grad)
    #     # print(now_size)

    #     # if now_grad consists of too few indices, consider all indices of the control tokens, just like GCG/DSN did
    #     if now_size <=1 : 
    #         now_size = 1
    #         now_grad = [_ for _ in range(len(self.control_toks))]

    #     # get the top-k best tokens per control suffix position/index
    #     top_gradient, top_indices = (-grad).topk(topk, dim=1)
    #     control_toks = self.control_toks.to(grad.device)
    #     # copy control tokens batchsize times
    #     original_control_toks = control_toks.repeat(batch_size, 1)

    #     # for each candidate suffix, randomly sample the indices from now_grad
    #     # how many indices are sampled is determined by now_size
    #     new_token_pos = torch.tensor(
    #         [np.random.choice(np.array(now_grad), size=now_size) for _ in range(batch_size)],
    #         device=grad.device,
    #         dtype=torch.int64
    #     )

    #     # for each row/candidate suffix, and for each position that ought to be modified
    #     # randomly pick a token from the top-k list for that position
    #     new_token_val = torch.gather(
    #         top_indices[new_token_pos], 2, 
    #         torch.randint(0, topk, (batch_size, new_token_pos.size(1), 1),
    #         device=grad.device)
    #     )

    #     # return the new control candidate tokens, where at position i, the new token value from the top-k list is inserted
    #     # so for each row/candidate suffix, replace the old token at the specified position with the newly sampled token
    #     # each candidate suffix might modify multiple tokens in the control suffix
    #     new_token_val = new_token_val.squeeze(-1)
    #     new_control_toks = original_control_toks.scatter_(1, new_token_pos, new_token_val)

    #     # print(new_control_toks.shape)
    #     return new_control_toks
    

class DSNMultiPromptAttack(MultiPromptAttack):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def step(self,
            batch_size=1024,
            topk=256,
            temp=1,
            allow_non_ascii=True,
            target_weight=1,
            control_weight=0.0,     # set to zero if not considered ppl
            verbose=False,
            filter_cand=True,
            current_step=None
        ):

        main_device = self.models[0].device
        # storage of candidate suffixes
        control_cands = []

        # each worker computes gradients wrt the control tokens
        # the gradients are computed over all goals and targets (the whole dataset)
        # refers to the grad function above in DSNAttackPrompt, which calls the token_gradients_dsn_loss func
        for j, worker in enumerate(self.workers):
            worker(self.prompts[j], "grad", worker.model)

        # Aggregate gradients
        grad = None
        # loop over the workers
        for j, worker in enumerate(self.workers):
            # get gradient tensor and normalize
            new_grad = worker.results.get().to(main_device)
            new_grad = new_grad / new_grad.norm(dim=-1, keepdim=True)
            if grad is None:                    
                grad = torch.zeros_like(new_grad)
            if grad.shape != new_grad.shape:   
                with torch.no_grad():
                    # generate candidate tokens
                    control_cand = self.prompts[j-1].sample_control(grad, batch_size, topk, temp, allow_non_ascii)
                    control_cands.append(self.get_filtered_cands(j-1, control_cand, filter_cand=filter_cand, curr_control=self.control_str))
                grad = new_grad
            else:
                grad += new_grad

        # grad is in shape length_control * vocabulary, 
        # e.g. in shape 20*32000
        with torch.no_grad():
            # generate candidate suffixes; we have batch_size number of candidates
            control_cand = self.prompts[j].sample_control(grad, batch_size, topk, temp, allow_non_ascii)
            del grad, new_grad
            torch.cuda.empty_cache()

            # before appending the candidates, first filter the ones out that are not tokenizer consistent
            control_cands.append(self.get_filtered_cands(j, control_cand, filter_cand=filter_cand, curr_control=self.control_str))

        del control_cand ; gc.collect()
        torch.cuda.empty_cache()

        # Search
        loss = torch.zeros(len(control_cands) * batch_size).to(main_device)             
        refusal_loss = torch.zeros(len(control_cands) * batch_size).to(main_device)     

        with torch.no_grad():
            # for each candidate suffix
            for j, cand in enumerate(control_cands):

                progress = tqdm( range(len(self.prompts[0])), total=len(self.prompts[0]) ) if verbose else enumerate(self.prompts[0])
                # for each prompt/goal and target
                for i in progress:

                    # for each worker/model, get the logits for each candidate suffix
                    for k, worker in enumerate(self.workers):

                        # gets logits after running the model on prompt[i]+candidate suffix 
                        worker(self.prompts[k][i], "logits", worker.model, test_controls = cand, return_ids=True)

                    # get model outputs/results for each worker
                    logits, ids = zip(*[worker.results.get() for worker in self.workers])

                    torch.cuda.empty_cache()
                    if self.para.debug_mode:
                        print('-'*15 + 'some debug info'+'-'*15)
                        pass

                    # compute target loss (the affirmative loss)
                    temp_gcg_loss = sum([
                        target_weight * self.prompts[k][i].target_loss(logit, id).to(main_device) # may already go through cosine decay
                        for k, (logit, id) in enumerate(zip(logits, ids))
                    ])
                    # save the loss at the right index for each candidate suffix
                    loss[ j*batch_size : (j+1)*batch_size ] += temp_gcg_loss

                    # in DSN: control_weight = 0
                    if control_weight != 0:     
                        print("computing control weight!")
                        loss[j*batch_size:(j+1)*batch_size] += sum([
                            control_weight*self.prompts[k][i].control_loss(logit, id).mean(dim=-1).to(main_device)
                            for k, (logit, id) in enumerate(zip(logits, ids))
                        ])

                    # in DSN: use_augmented_loss=True, so it uses refusal loss
                    if not self.para.use_augmented_loss:
                        overall_loss = loss
                    elif self.para.use_augmented_loss:    # DSN loss = affirmative loss + refusal loss
                        # compute the refusal loss; refers to the dsn_refusal_loss func from AttackPrompt class
                        refusal_loss[ j*batch_size : (j+1)*batch_size ] += sum([
                            target_weight * self.prompts[k][i].dsn_refusal_loss(logit, id).to(main_device)
                            for k, (logit, id) in enumerate(zip(logits, ids))
                        ])
                        # final loss = affirmative loss + refusal loss
                        # --> so for every candidate suffix, the loss and refusal loss
                        # will eventually, after this loop, be computed across/over all prompts/goals
                        overall_loss = loss + refusal_loss
                        print('refusal loss shape', refusal_loss.shape)

                    del logits, ids; gc.collect()
                    torch.cuda.empty_cache()

                    # in DSN verbose = True
                    if verbose:                 
                        progress.set_description(f"loss={loss[j*batch_size:(j+1)*batch_size].min().item()/(i+1):.4f}")

            # find lowest loss; aka find idx of the best suffix with the smallest loss
            print('overall loss shape', overall_loss.shape)
            print('overall loss', overall_loss)
            print('loss shape', loss.shape)
            min_idx = overall_loss.argmin()
            model_idx = min_idx // batch_size
            batch_idx = min_idx % batch_size
            # pick best suffix/get the best suffix tokens, and obtain the corresponding lowest loss
            next_control, cand_loss = control_cands[model_idx][batch_idx], overall_loss[min_idx]

            # normalize the loss over the goals and workers
            loss_wrt_whole_ctrl = (overall_loss/len(self.prompts[0])/len(self.workers)).tolist()

        # to store two loss term during each step into a pth file
        logfile = self.para.result_prefix
        if logfile.endswith('.json'):
            loss_his_path = deepcopy(logfile)
            loss_his_path = loss_his_path.replace('.json', '_loss_history@step')

        if current_step == 1:
            store_gcg_loss_history_previous = []
            store_refusal_loss_history_previous = []
        else:
            temp_loss_dict = torch.load(loss_his_path+f"{current_step-1}.pth")
            store_gcg_loss_history_previous = temp_loss_dict['gcg']
            store_refusal_loss_history_previous = temp_loss_dict['refusal']

        store_gcg_loss_history = [loss[min_idx].item() / len(self.prompts[0]) / len(self.workers)]
        store_refusal_loss_history = [refusal_loss[min_idx].item() / len(self.prompts[0]) / len(self.workers)]
        dual_loss_his = {
            'gcg':store_gcg_loss_history_previous + store_gcg_loss_history,
            'refusal':store_refusal_loss_history_previous + store_refusal_loss_history
            }
        # logging 
        torch.save(dual_loss_his, loss_his_path+f"{current_step-1}.pth")
        os.rename(loss_his_path+f"{current_step-1}.pth", loss_his_path+f"{current_step}.pth")

        del loss, refusal_loss, overall_loss ; gc.collect()
        torch.cuda.empty_cache()

        tokenize_offset = 0
        if "Qwen2-7B-Instruct" in self.para.model_paths[0]:
            tokenize_offset = 1

        output_temp_str = 'Current length: '
        output_temp_str += str( len(self.workers[0].tokenizer(next_control).input_ids[1:])+tokenize_offset )
        output_temp_str += ' the adv suffix is now:'

        if self.logger is None:         # output by print
            print(output_temp_str)
            print(next_control)
        else:                           # output in the logger!
            self.logger.info(output_temp_str)
            self.logger.info(next_control)
        del output_temp_str

        # returns best adversarial suffix found in this step, avg loss per goal and model, control candidates of the 1st batch, and all cand losses
        return next_control, cand_loss.item() / len(self.prompts[0]) / len(self.workers), (control_cands[0], loss_wrt_whole_ctrl)