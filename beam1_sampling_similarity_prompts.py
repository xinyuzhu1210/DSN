harmbench_advbench = []
gemma_advbench = []
harmbench_jbb = []
gemma_jbb = []
rm_advbench_list = []
rm_jbb_list = []

h_advbench = False
g_advbench = False
h_jbb = False
g_jbb = False
rm_advbench = False
rm_jbb = False

# prompt file for beam=1
with open('beam1_output.txt', 'r') as file:
    for line in file:
        # obtain harmbench advbench prompts
        if "harmbench advbench prompts" in line.strip():
            h_advbench = True
        if "gemma advbench prompts" in line.strip():
            g_advbench = True
            h_advbench = False
        if h_advbench == True and not "harmbench advbench prompts" in line.strip():
            harmbench_advbench.append(line.strip())   
        # obtain gemma advbench prompts  
        if "harmbench jbb prompts" in line.strip():
            g_advbench = False
            h_jbb = True
        if g_advbench == True and not "gemma advbench prompts" in line.strip():
            gemma_advbench.append(line.strip())
        # obtain harmbench jbb prompts
        if "gemma jbb prompts" in line.strip(): 
            h_jbb = False
            g_jbb = True
        if h_jbb == True and not "harmbench jbb prompts" in line.strip():
            harmbench_jbb.append(line.strip())
        # obtain gemma jbb prompts
        if "rm advbench prompts" in line.strip():
            g_jbb = False
            rm_advbench = True
        if g_jbb == True and not "gemma jbb prompts" in line.strip():
            gemma_jbb.append(line.strip())
        # obtain rm advbench prompts
        if "rm jbb prompts" in line.strip():
            rm_advbench = False
            rm_jbb = True
        if rm_advbench == True and not "rm advbench prompts" in line.strip():
            rm_advbench_list.append(line.strip())
        # obtain rm jbb prompts
        if rm_jbb == True and not "rm jbb prompts" in line.strip():
            rm_jbb_list.append(line.strip())

harmbench_advbench_sampling = []
gemma_advbench_sampling = []
harmbench_jbb_sampling = []
gemma_jbb_sampling = []
rm_advbench_list_sampling = []
rm_jbb_list_sampling = []

h_advbench = False
g_advbench = False
h_jbb = False
g_jbb = False
rm_advbench = False
rm_jbb = False

# prompt file for sampling
with open('sampling.txt', 'r') as file:
    for line in file:
        # obtain harmbench advbench prompts
        if "harmbench advbench prompts" in line.strip():
            h_advbench = True
        if "gemma advbench prompts" in line.strip():
            g_advbench = True
            h_advbench = False
        if h_advbench == True and not "harmbench advbench prompts" in line.strip():
            harmbench_advbench_sampling.append(line.strip())   
        # obtain gemma advbench prompts  
        if "harmbench jbb prompts" in line.strip():
            g_advbench = False
            h_jbb = True
        if g_advbench == True and not "gemma advbench prompts" in line.strip():
            gemma_advbench_sampling.append(line.strip())
        # obtain harmbench jbb prompts
        if "gemma jbb prompts" in line.strip(): 
            h_jbb = False
            g_jbb = True
        if h_jbb == True and not "harmbench jbb prompts" in line.strip():
            harmbench_jbb_sampling.append(line.strip())
        # obtain gemma jbb prompts
        if "rm advbench prompts" in line.strip():
            g_jbb = False
            rm_advbench = True
        if g_jbb == True and not "gemma jbb prompts" in line.strip():
            gemma_jbb_sampling.append(line.strip())
        # obtain rm advbench prompts
        if "rm jbb prompts" in line.strip():
            rm_advbench = False
            rm_jbb = True
        if rm_advbench == True and not "rm advbench prompts" in line.strip():
            rm_advbench_list_sampling.append(line.strip())
        # obtain rm jbb prompts
        if rm_jbb == True and not "rm jbb prompts" in line.strip():
            rm_jbb_list_sampling.append(line.strip())


# overlap rm advbench prompts between beam=1 and sampling case
overlap_rm_adv_prompts = set(rm_advbench_list) & set(rm_advbench_list_sampling)
# remove new lines or empty lines
rm_advbench_list = [x for x in rm_advbench_list if x.strip()]
rm_advbench_list_sampling = [x for x in rm_advbench_list_sampling if x.strip()]
overlap_rm_adv_prompts = [x for x in overlap_rm_adv_prompts if x.strip()]
# calculate the unique items for the jaccard similarity
unique_items_1 = len(rm_advbench_list) + len(rm_advbench_list_sampling) - len(overlap_rm_adv_prompts)

# overlap rm jbb prompts
overlap_rm_jbb_prompts = set(rm_jbb_list) & set(rm_jbb_list_sampling)
# remove new lines or empty lines
rm_jbb_list = [x for x in rm_jbb_list if x.strip()]
rm_jbb_list_sampling = [x for x in rm_jbb_list_sampling if x.strip()]
overlap_rm_jbb_prompts = [x for x in overlap_rm_jbb_prompts if x.strip()]
# calculate the unique items for the jaccard similarity
unique_items_2 = len(rm_jbb_list) + len(rm_jbb_list_sampling) - len(overlap_rm_jbb_prompts)

# overlap harmbench advbench prompts
overlap_harmbench_adv_prompts = set(harmbench_advbench) & set(harmbench_advbench_sampling)
# remove new lines or empty lines
harmbench_advbench = [x for x in harmbench_advbench if x.strip()]
harmbench_advbench_sampling = [x for x in harmbench_advbench_sampling if x.strip()]
overlap_harmbench_adv_prompts = [x for x in overlap_harmbench_adv_prompts if x.strip()]
# calculate the unique items for the jaccard similarity
unique_items_3 = len(harmbench_advbench) + len(harmbench_advbench_sampling) - len(overlap_harmbench_adv_prompts)

# overlap gemma advbench prompts
overlap_gemma_adv_prompts = set(gemma_advbench) & set(gemma_advbench_sampling)
# remove new lines or empty lines
gemma_advbench = [x for x in gemma_advbench if x.strip()]
gemma_advbench_sampling = [x for x in gemma_advbench_sampling if x.strip()]
overlap_gemma_adv_prompts = [x for x in overlap_gemma_adv_prompts if x.strip()]
# calculate the unique items for the jaccard similarity
unique_items_4 = len(gemma_advbench) + len(gemma_advbench_sampling) - len(overlap_gemma_adv_prompts)

# overlap harmbench jbb prompts
overlap_harmbench_jbb_prompts = set(harmbench_jbb) & set(harmbench_jbb_sampling)
# remove new lines or empty lines
harmbench_jbb = [x for x in harmbench_jbb if x.strip()]
harmbench_jbb_sampling = [x for x in harmbench_jbb_sampling if x.strip()]
overlap_harmbench_jbb_prompts = [x for x in overlap_harmbench_jbb_prompts if x.strip()]
# calculate the unique items for the jaccard similarity
unique_items_5 = len(harmbench_jbb) + len(harmbench_jbb_sampling) - len(overlap_harmbench_jbb_prompts)

# overlap gemma jbb prompts
overlap_gemma_jbb_prompts = set(gemma_jbb) & set(gemma_jbb_sampling)
# remove new lines or empty lines
gemma_jbb = [x for x in gemma_jbb if x.strip()]
gemma_jbb_sampling = [x for x in gemma_jbb_sampling if x.strip()]
overlap_gemma_jbb_prompts = [x for x in overlap_gemma_jbb_prompts if x.strip()]
# calculate the unique items for the jaccard similarity
unique_items_6 = len(gemma_jbb) + len(gemma_jbb_sampling) - len(overlap_gemma_jbb_prompts)

# print jaccard similarity
print(f"overlap rm advbench prompts = {len(overlap_rm_adv_prompts)}/{unique_items_1} ({(len(overlap_rm_adv_prompts)/unique_items_1 ) * 100}%)")
print(f"overlap rm jbb prompts = {len(overlap_rm_jbb_prompts)}/{unique_items_2} ({(len(overlap_rm_jbb_prompts)/unique_items_2 ) * 100}%)")
print(f"overlap harmbench advbench prompts = {len(overlap_harmbench_adv_prompts)}/{unique_items_3} ({(len(overlap_harmbench_adv_prompts)/unique_items_3 ) * 100}%)")
print(f"overlap gemma advbench prompts = {len(overlap_gemma_adv_prompts)}/{unique_items_4} ({(len(overlap_gemma_adv_prompts)/unique_items_4 ) * 100}%)")
print(f"overlap harmbench jbb prompts = {len(overlap_harmbench_jbb_prompts)}/{unique_items_5} ({(len(overlap_harmbench_jbb_prompts)/unique_items_5 ) * 100}%)")
print(f"overlap gemma jbb prompts = {len(overlap_gemma_jbb_prompts)}/{unique_items_6} ({(len(overlap_gemma_jbb_prompts)/unique_items_6 ) * 100}%)")
