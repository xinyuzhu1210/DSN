# advbench
harmbench_prompts_beam1 = []
harmbench_outputs_beam1 = []
gemma4_prompts_beam1 = []
gemma4_outputs_beam1 = []
# get path to Harmbench and Gemma beam=1 or sampling output file for the advbench dataset 
# with open('../../../Desktop/beam_search_additional_experiment_qwen_DSN/beam1/seed_45/harmbench_gemma_advbench/slurm_output_23031557.out', 'r') as file:
with open('../../../Desktop/beam_search_additional_experiment_qwen_DSN/sampling/seed_45/harmbench_gemma_advbench/slurm_output_23030269.out', 'r') as file:
    for line in file:
        # at each goal/prompt, add the harmbench and gemma4 responses to the list
        if "Harmbench goal" in line.strip():
            harmbench_prompts_beam1.append(line.strip())
        if "Harmbench classification" in line.strip():
            harmbench_outputs_beam1.append(line.strip())
        if "Gemma4 goal" in line.strip():
            gemma4_prompts_beam1.append(line.strip())
        if "Gemma4 classification" in line.strip():
            gemma4_outputs_beam1.append(line.strip())

harmbench_prompts_beam9 = []
harmbench_outputs_beam9 = []
gemma4_prompts_beam9 = []
gemma4_outputs_beam9 = []

# get path to Harmbench and Gemma beam=9 output file for the advbench dataset
with open('../../../Desktop/beam_search_additional_experiment_qwen_DSN/beam9/seed_45/harmbench_gemma_advbench/slurm_output_23031018.out', 'r') as file:
    for line in file:
        # at each goal/prompt, add the harmbench and gemma4 responses to the list
        if "Harmbench goal" in line.strip():
            harmbench_prompts_beam9.append(line.strip())
        if "Harmbench classification" in line.strip():
            harmbench_outputs_beam9.append(line.strip())
        if "Gemma4 goal" in line.strip():
            gemma4_prompts_beam9.append(line.strip())
        if "Gemma4 classification" in line.strip():
            gemma4_outputs_beam9.append(line.strip())

harmbench_correct_scores = 0
# count total nr of rejections from the harmbench classifier in the beam=9 case
harmbench_total_negatives_beam9 = harmbench_outputs_beam9.count("Harmbench classification No")
gemma4_correct_scores = 0
# count total nr of rejections from the Gemma4 classifier in the beam=9 case
gemma4_total_negatives_beam9 = gemma4_outputs_beam9.count("Gemma4 classification no")

harmbench_prompts = []
gemma_prompts = []

for i in range(len(harmbench_prompts_beam9)):
    # count for harmbench and gemma4 how many from the rejected prompts in the beam=9 case, were actually accepted in the greedy (beam=1) case
    if harmbench_outputs_beam9[i] == "Harmbench classification No" and harmbench_outputs_beam1[i] == "Harmbench classification Yes":
        harmbench_correct_scores += 1
        harmbench_prompts.append(f"prompt {i}: {harmbench_prompts_beam1[i]}")
    if gemma4_outputs_beam9[i] == "Gemma4 classification no" and gemma4_outputs_beam1[i] == "Gemma4 classification yes":
        gemma4_correct_scores += 1
        gemma_prompts.append(f"prompt {i}: {gemma4_prompts_beam1[i]}")

print("harmbench advbench prompts")
for i in harmbench_prompts: 
    print(i)

print("gemma advbench prompts")
for i in gemma_prompts: 
    print(i)

# print the total scores for both classifiers for the advbench dataset 
print("Harmbench and Gemma4 advbench dataset")
print(f"There are {harmbench_correct_scores}/{harmbench_total_negatives_beam9} ({(harmbench_correct_scores/harmbench_total_negatives_beam9) * 100}%) beam=1/sampling accepted cases for Harmbench.")
print(f"There are {gemma4_correct_scores}/{gemma4_total_negatives_beam9} ({(gemma4_correct_scores/gemma4_total_negatives_beam9) * 100}%) beam=1/sampling accepted cases for Gemma4.")


# jailbreakbench
harmbench_prompts_beam1 = []
harmbench_outputs_beam1 = []
gemma4_prompts_beam1 = []
gemma4_outputs_beam1 = []
# get path to Harmbench and Gemma beam=1 or sampling output file for the jailbreakbench dataset
# with open('../../../Desktop/beam_search_additional_experiment_qwen_DSN/beam1/seed_45/harmbench_gemma_jbb/slurm_output_23031694.out', 'r') as file:
with open('../../../Desktop/beam_search_additional_experiment_qwen_DSN/sampling/seed_45/harmbench_gemma_jbb/slurm_output_23030378.out', 'r') as file:
    for line in file:
        # at each goal/prompt, add the harmbench and gemma4 responses to the list
        if "Harmbench goal" in line.strip():
            harmbench_prompts_beam1.append(line.strip())
        if "Harmbench classification" in line.strip():
            harmbench_outputs_beam1.append(line.strip())
        if "Gemma4 goal" in line.strip():
            gemma4_prompts_beam1.append(line.strip())
        if "Gemma4 classification" in line.strip():
            gemma4_outputs_beam1.append(line.strip())

harmbench_prompts_beam9 = []
harmbench_outputs_beam9 = []
gemma4_prompts_beam9 = []
gemma4_outputs_beam9 = []

# get path to Harmbench and Gemma beam=9 output file for the jailbreakbench dataset
with open('../../../Desktop/beam_search_additional_experiment_qwen_DSN/beam9/seed_45/harmbench_gemma_jbb/slurm_output_23031142.out', 'r') as file:
    for line in file:
        # at each goal/prompt, add the harmbench and gemma4 responses to the list
        if "Harmbench goal" in line.strip():
            harmbench_prompts_beam9.append(line.strip())
        if "Harmbench classification" in line.strip():
            harmbench_outputs_beam9.append(line.strip())
        if "Gemma4 goal" in line.strip():
            gemma4_prompts_beam9.append(line.strip())
        if "Gemma4 classification" in line.strip():
            gemma4_outputs_beam9.append(line.strip())

harmbench_correct_scores = 0
# count total nr of rejections from the harmbench classifier in the beam=9 case
harmbench_total_negatives_beam9 = harmbench_outputs_beam9.count("Harmbench classification No")
gemma4_correct_scores = 0
# count total nr of rejections from the Gemma4 classifier in the beam=9 case
gemma4_total_negatives_beam9 = gemma4_outputs_beam9.count("Gemma4 classification no")

harmbench_prompts = []
gemma_prompts = []

for i in range(len(harmbench_prompts_beam9)):
    # count for harmbench and gemma4 how many from the rejected prompts in the beam=9 case, were actually accepted in the greedy (beam=1) case
    if harmbench_outputs_beam9[i] == "Harmbench classification No" and harmbench_outputs_beam1[i] == "Harmbench classification Yes":
        harmbench_correct_scores += 1
        harmbench_prompts.append(f"prompt {i}: {harmbench_prompts_beam1[i]}")
    if gemma4_outputs_beam9[i] == "Gemma4 classification no" and gemma4_outputs_beam1[i] == "Gemma4 classification yes":
        gemma4_correct_scores += 1
        gemma_prompts.append(f"prompt {i}: {gemma4_prompts_beam1[i]}")

print("harmbench jbb prompts")
for i in harmbench_prompts: 
    print(i)

print("gemma jbb prompts")
for i in gemma_prompts: 
    print(i)

# print the total scores for both classifiers for the jailbreakbench dataset
print("Harmbench and Gemma4 jailbreakbench dataset")
print(f"There are {harmbench_correct_scores}/{harmbench_total_negatives_beam9} ({(harmbench_correct_scores/harmbench_total_negatives_beam9) * 100}%) beam=1/sampling accepted cases for Harmbench.")
print(f"There are {gemma4_correct_scores}/{gemma4_total_negatives_beam9} ({(gemma4_correct_scores/gemma4_total_negatives_beam9) * 100}%) beam=1/sampling accepted cases for Gemma4.")


# Refusal Matching
RM_targets_advbench_beam1 = []
RM_outputs_advbench_beam1 = []
RM_targets_jbb_beam1 = []
RM_outputs_jbb_beam1 = []
training_samples_passed = False
jbb_dataset = False
# get path to refusal matching beam=1 or sampling output file 
# with open('../../../Desktop/beam_search_additional_experiment_qwen_DSN/beam1/seed_45/refusal_matching/slurm_output_23031310.out', 'r') as file:
with open('../../../Desktop/beam_search_additional_experiment_qwen_DSN/sampling/seed_45/refusal_matching/slurm_output_23029910.out', 'r') as file:
    for line in file:
        # do not include the evaluation results from the advbench training data
        if "Train Step" in line.strip():
            training_samples_passed = True
        # at each goal/prompt, add the refusal matching classifier responses of the advbench dataset to the list
        if "target string" in line.strip() and training_samples_passed == True and jbb_dataset == False:
            RM_targets_advbench_beam1.append(line.strip())
        if "classifier 2" in line.strip() and training_samples_passed == True and jbb_dataset == False:
            RM_outputs_advbench_beam1.append(line.strip())
        # now only include samples of the jailbreakbench dataset
        if "logfile= ../evalJBBLastStep" in line.strip() and training_samples_passed == True: 
            jbb_dataset = True
        # at each goal/prompt, add the refusal matching classifier responses of the jailbreakbench dataset to the list
        if "target string" in line.strip() and training_samples_passed == True and jbb_dataset == True:
            RM_targets_jbb_beam1.append(line.strip())
        if "classifier 2" in line.strip() and training_samples_passed == True and jbb_dataset == True:
            RM_outputs_jbb_beam1.append(line.strip())


RM_targets_advbench_beam9 = []
RM_outputs_advbench_beam9 = []
RM_targets_jbb_beam9 = []
RM_outputs_jbb_beam9 = []
training_samples_passed = False
jbb_dataset = False
# get path to the refusal matching beam=9 output file 
with open('../../../Desktop/beam_search_additional_experiment_qwen_DSN/beam9/seed_45/refusal_matching/slurm_output_23030825.out', 'r') as file:
    for line in file:
        # do not include the evaluation results from the advbench training data
        if "Train Step" in line.strip():
            training_samples_passed = True
        # at each goal/prompt, add the refusal matching classifier responses of the advbench dataset to the list
        if "target string" in line.strip() and training_samples_passed == True and jbb_dataset == False:
            RM_targets_advbench_beam9.append(line.strip())
        if "classifier 2" in line.strip() and training_samples_passed == True and jbb_dataset == False:
            RM_outputs_advbench_beam9.append(line.strip())
        # now only include samples of the jailbreakbench dataset
        if "logfile= ../evalJBBLastStep" in line.strip() and training_samples_passed == True: 
            jbb_dataset = True
        # at each goal/prompt, add the refusal matching classifier responses of the jailbreakbench dataset to the list
        if "target string" in line.strip() and training_samples_passed == True and jbb_dataset == True:
            RM_targets_jbb_beam9.append(line.strip())
        if "classifier 2" in line.strip() and training_samples_passed == True and jbb_dataset == True:
            RM_outputs_jbb_beam9.append(line.strip())

advbench_correct_scores = 0
advbench_total_negatives_beam9 = 0
jbb_correct_scores = 0
jbb_total_negatives_beam9 = 0

rm_advbench = []
rm_jbb = []

for i in range(len(RM_targets_advbench_beam9)):
    # count how many from the rejected prompts in the beam=9 case, were actually accepted in the greedy (beam=1) case for the advbench dataset
    if ("LABEL_1" in RM_outputs_advbench_beam9[i] or "LABEL_3" in RM_outputs_advbench_beam9[i]) and ("LABEL_0" in RM_outputs_advbench_beam1[i] or "LABEL_2" in RM_outputs_advbench_beam1[i] or "LABEL_4" in RM_outputs_advbench_beam1[i]):
        advbench_correct_scores += 1
        rm_advbench.append(f"prompt advbench {i}: {RM_targets_advbench_beam1[i]}")
    # count total nr of rejections in the beam=9 case
    if "LABEL_1" in RM_outputs_advbench_beam9[i] or "LABEL_3" in RM_outputs_advbench_beam9[i]:
        advbench_total_negatives_beam9 += 1
    # count how many from the rejected prompts in the beam=9 case, were actually accepted in the greedy (beam=1) case for the jailbreakbench dataset
    if ("LABEL_1" in RM_outputs_jbb_beam9[i] or "LABEL_3" in RM_outputs_jbb_beam9[i]) and ("LABEL_0" in RM_outputs_jbb_beam1[i] or "LABEL_2" in RM_outputs_jbb_beam1[i] or "LABEL_4" in RM_outputs_jbb_beam1[i]):
        jbb_correct_scores += 1
        rm_jbb.append(f"prompt jbb {i}: {RM_targets_jbb_beam1[i]}")
    # count total nr of rejections in the beam=9 case
    if "LABEL_1" in RM_outputs_jbb_beam9[i] or "LABEL_3" in RM_outputs_jbb_beam9[i]:
        jbb_total_negatives_beam9 += 1

print("rm advbench prompts")
for i in rm_advbench: 
    print(i)

print("rm jbb prompts")
for i in rm_jbb: 
    print(i)

# print the total scores for refusal matching metric
print("Refusal Matching")
print(f"There are {advbench_correct_scores}/{advbench_total_negatives_beam9} ({(advbench_correct_scores/advbench_total_negatives_beam9) * 100}%) beam=1/sampling accepted cases for Advbench.")
print(f"There are {jbb_correct_scores}/{jbb_total_negatives_beam9} ({(jbb_correct_scores/jbb_total_negatives_beam9) * 100}%) beam=1/sampling accepted cases for JBB")
