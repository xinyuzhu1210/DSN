import time
import os
import shutil
import json
import pandas as pd
import csv
from pathlib import Path
import httpx
import sys

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import spacy
from spacy.language import Language
import numpy as np
from tqdm import tqdm
from transformers.trainer_utils import set_seed 

os.sys.path.append("..")

from eval_ensemble_src.get_everything import get_goals_and_targets
from eval_ensemble_src.eval4_HarmBench import get_HarmBench_results

def get_model_name(log_file_path):
    if "vicuna13bv15" in log_file_path:
        return 'vicuna-13b-v1.5'
    elif "vicuna" in log_file_path:
        return 'Vicuna-7B'
    elif "llama31" in log_file_path:
        return 'LLaMA-3.1-8B'
    elif "llama3" in log_file_path:
        return 'LLaMA-3-8B'
    elif "llama2-13b" in log_file_path:
        return 'Llama-2-13b-chat-hf'
    elif "llama" in log_file_path:
        return 'LLaMA-2-7B'
    elif "mistralv03" in log_file_path:
        return 'Mistral-7B-Instruct-v0.3'
    elif "mistral" in log_file_path:
        return 'Mistral-7B-Instruct-v0.2'
    elif "gemma9b" in log_file_path:
        return 'gemma-2-9b-it'
    elif "qwen" in log_file_path:
        return 'Qwen2-7B-Instruct'
    else:
        return None

def main():
    # random seed refers to the first arg in launch_harmbench_eval.sh
    random_seed = int(sys.argv[1])
    # logfile path refers to the second arg in launch_harmbench_eval.sh
    log_file_path = sys.argv[2]
    # whether or not to use the JBB dataset refers to the third arg in launch_harmbench_eval.sh
    use_jailbreakbench = eval(sys.argv[3])

    assert isinstance(random_seed, int)
    assert isinstance(log_file_path, str)

    set_seed(random_seed)

    # if os.path.exists(os.path.join(os.path.dirname(log_file_path), "results_HarmBench.json")):
    #     print("Already run...")
    #     return None

    print(f"The log_file_path is {log_file_path}")
    start = time.time()    
    # get model name
    model_name = get_model_name(log_file_path)

    with open(log_file_path, 'r') as f:
        log = json.load(f)

    n_train_data = 0 if use_jailbreakbench else 25
    # get the data
    train_goals, train_targets, test_goals, test_targets = get_goals_and_targets(n_train_data=n_train_data, sampling_seed=random_seed, use_jailbreakbench=use_jailbreakbench)

    # get the latest/final test outputs and Refusal Matching jailbreak results 
    test_outputs = log[model_name]['test_outputs'][-1]
    test_jb_KWM = log[model_name]['test_jb'][-1]
    # total nr of jailbreak sucesses
    test_jb_ASR = sum(test_jb_KWM)

    # duplicate the tested (last) suffix for all test goals
    all_ctrl = [log["Tested suffix"][-1]]*len(test_goals)

    # evaluate with HarmBench
    results_HarmBench = []
    for i, (goal, answer, ctrl) in tqdm(enumerate(zip(test_goals, test_outputs, all_ctrl)), total=len(test_goals)):
        # use the harmbench classifier on the test goals, outputs and adversarial control tokens
        # it will return True or False
        results_HarmBench.append(get_HarmBench_results(goal, answer, ctrl, contains_suffix=True))
    torch.cuda.empty_cache()
    print("the HarmBench evaluator is done")

    # list of refusal matching results (consisting of True and False)
    RM = test_jb_KWM
    # list of harmbench results (consisting of True and False)
    HB = results_HarmBench

    # logging and save the results
    parent_folder = os.path.dirname(log_file_path)
    # new_eval_file_path = os.path.join(parent_folder, "results_HarmBench.json")
    # new_eval_file_path = os.path.join(parent_folder, "results_qwen3.5.json")
    new_eval_file_path = os.path.join(parent_folder, "results_gemma4.json")

    with open(new_eval_file_path, 'w', encoding='utf-8') as json_file:
        current_time = time.strftime("%Y%m%d-%H:%M:%S")
        json.dump(
            {
                "Refusal_KWM_ASR":test_jb_ASR,
                "results_refusal":RM,
                "results_HB":results_HarmBench,
                "test_goals":test_goals,
                "test_outputs":test_outputs,
                "eval_time":current_time
            },
            json_file, ensure_ascii=False, indent=4)
        print(f"{new_eval_file_path} has been saved, time taken is {time.time() - start} seconds, now is {current_time}")

    # print(f"Refusal Matching Score: {test_jb_ASR} / {len(RM)} | Harmbench score: {sum(results_HarmBench)} / {len(results_HarmBench)}")
    # print(f"Refusal Matching Score: {test_jb_ASR} / {len(RM)} | Qwen3.5 score: {sum(results_HarmBench)} / {len(results_HarmBench)}")
    print(f"Refusal Matching Score: {test_jb_ASR} / {len(RM)} | Gemma4-26B A4B score: {sum(results_HarmBench)} / {len(results_HarmBench)}")
    
    print('Harmbench evaluation is done!')

if __name__ == '__main__':
    main()