#!/bin/bash

export n=25
export model=llama31 # choose from: gemma, gemma2, llama2, llama2_13b, llama3, llama31, mistralv02, mistralv03, qwen, vicuna_13b, vicuna

# sample file path, select the corresponding file path please
# llama31
# ../results_dsn/20260127-03:30:44 1E0/llama31_dsn_25_offset0.json
# ../results_dsn/20260127-14:25:13 1E0/llama31_dsn_25_offset0.json
# ../results_dsn/20260128-01:18:36 1E0/llama31_dsn_25_offset0.json
# ../results_dsn/20260128-13:47:22 1E0/llama31_dsn_25_offset0.json
# qwen
# ../results_dsn/20260203-02:01:22 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260203-02:04:40 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260203-02:06:12 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260203-02:07:25 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260203-02:09:25 1E0/qwen_dsn_25_offset0.json
# llama3
# ../results_dsn/20260203-20:01:23 1E0/llama3_dsn_25_offset0.json
# ../results_dsn/20260203-20:05:44 1E0/llama3_dsn_25_offset0.json
# ../results_dsn/20260203-20:07:35 1E0/llama3_dsn_25_offset0.json
# ../results_dsn/20260203-20:09:50 1E0/llama3_dsn_25_offset0.json
# ../results_dsn/20260203-20:11:07 1E0/llama3_dsn_25_offset0.json
# qwen batch_size 41, 42, 43, 44, 45, aug_sampling = false
# ../results_dsn/20260206-17:12:43 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260209-19:52:54 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260209-19:56:48 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260209-19:58:46 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260209-20:22:30 1E0/qwen_dsn_25_offset0.json

# qwen batch_size 41, 42, 43, 44, 45, aug_sampling = true
# ../results_dsn/20260209-23:12:54 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260210-15:16:19 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260210-14:50:10 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260210-15:06:41 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260210-15:08:15 1E0/qwen_dsn_25_offset0.json
# Qwen2-7B batch size 256, seed 41, 42, 43, 44, 45, use_aug_sampling=False, topk=10
# ../results_dsn/20260214-00:37:15 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260214-00:39:58 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260214-00:41:13 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260214-00:42:30 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260214-00:43:43 1E0/qwen_dsn_25_offset0.json
# Qwen2-7B train, batch size 256, seed 41, 42, 43, 44, 45, use_aug_sampling=False, doubled prefixes list
# ../results_dsn/20260214-01:14:28 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260214-01:17:29 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260214-01:18:57 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260214-01:20:00 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260216-18:34:40 1E0/qwen_dsn_25_offset0.json
# Qwen2-7B train, batch size 256, seed 41, 42, 43, 44, 45, use_aug_sampling=False, Magic integration
# ../results_dsn/20260311-04:27:52 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260311-04:30:23 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260311-04:33:09 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260311-04:35:24 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260311-04:36:33 1E0/qwen_dsn_25_offset0.json
# Qwen same seed 41 test
# ../results_dsn/20260206-17:12:43 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260206-17:14:48 1E0/qwen_dsn_25_offset0.json
# Qwen tripled list of refusal words
# ../results_dsn/20260326-02:09:41 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260326-02:18:06 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260326-02:20:49 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260326-02:22:11 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260326-02:24:37 1E0/qwen_dsn_25_offset0.json
# Qwen tripled list seed 42 top-k average
# ../results_dsn/20260410-01:04:26 1E0/qwen_dsn_25_offset0.json
# Qwen tripled list seed 42 max() operation
# ../results_dsn/20260414-00:58:27 1E0/qwen_dsn_25_offset0.json
# Qwen original list seed 42 top-k average
# ../results_dsn/20260414-02:57:13 1E0/qwen_dsn_25_offset0.json
# Qwen original list seed 42 max() operation
# ../results_dsn/20260414-02:54:44 1E0/qwen_dsn_25_offset0.json

# qwen original list top-10% of variance windows seed 42
# ../results_dsn/20260506-02:36:34 1E0/qwen_dsn_25_offset0.json
# qwen tripled list top-10% of variance windows seed 42
# ../results_dsn/20260506-02:38:57 1E0/qwen_dsn_25_offset0.json
# qwen original list top-10% of entropy windows seed 42
# ../results_dsn/20260506-02:23:36 1E0/qwen_dsn_25_offset0.json
# qwen tripled list top-10% of entropy windows seed 42
# ../results_dsn/20260506-02:28:30 1E0/qwen_dsn_25_offset0.json 

# qwen seed 42 half of list
# ../results_dsn/20260526-04:37:59 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260518-23:00:20 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260526-04:42:18 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260526-04:44:02 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260526-04:46:16 1E0/qwen_dsn_25_offset0.json

# qwen seed 42 curated list
# ../results_dsn/20260526-04:49:15 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260520-00:47:50 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260526-04:51:02 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260526-04:52:33 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260526-04:54:55 1E0/qwen_dsn_25_offset0.json

# qwen batch_size 41, 42, 43, 44, 45, aug_sampling = false 
# ../results_dsn/20260206-17:12:43 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260209-19:52:54 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260209-19:56:48 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260209-19:58:46 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260209-20:22:30 1E0/qwen_dsn_25_offset0.json

# qwen GCG seeds 41, 42, 43, 44, 45
# ../results_dsn/20260526-05:07:02 1EOriginal/qwen_dsn_25_offset0.json
# ../results_dsn/20260526-05:09:39 1EOriginal/qwen_dsn_25_offset0.json
# ../results_dsn/20260526-05:13:05 1EOriginal/qwen_dsn_25_offset0.json
# ../results_dsn/20260526-05:15:03 1EOriginal/qwen_dsn_25_offset0.json
# ../results_dsn/20260526-05:20:00 1EOriginal/qwen_dsn_25_offset0.json

# qwen DSN no seed (1x original rm method)
# ../results_dsn/20260203-02:01:22 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260203-02:04:40 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260203-02:06:12 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260203-02:07:25 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260203-02:09:25 1E0/qwen_dsn_25_offset0.json

# Qwen2-7B train, batch size 256, seed 41, 42, 43, 44, 45, use_aug_sampling=False, Magic integration
# ../results_dsn/20260311-04:27:52 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260311-04:30:23 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260311-04:33:09 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260311-04:35:24 1E0/qwen_dsn_25_offset0.json
# ../results_dsn/20260311-04:36:33 1E0/qwen_dsn_25_offset0.json

# llama31 no seed
# ../results_dsn/20260127-03:30:44 1E0/llama31_dsn_25_offset0.json
# ../results_dsn/20260127-14:25:13 1E0/llama31_dsn_25_offset0.json
# ../results_dsn/20260128-01:18:36 1E0/llama31_dsn_25_offset0.json
# ../results_dsn/20260128-13:47:22 1E0/llama31_dsn_25_offset0.json
# ../results_dsn/20260603-05:45:04 1E0/llama31_dsn_25_offset0.json

# llama31 with seeds 41 42 43 44 45 batchsize 512
# ../results_dsn/20260603-05:49:54 1E0/llama31_dsn_25_offset0.json
# ../results_dsn/20260603-05:54:17 1E0/llama31_dsn_25_offset0.json
# ../results_dsn/20260603-05:56:13 1E0/llama31_dsn_25_offset0.json
# ../results_dsn/20260603-05:57:22 1E0/llama31_dsn_25_offset0.json
# ../results_dsn/20260603-05:58:48 1E0/llama31_dsn_25_offset0.json

# llama31 GCG seeds 41 42 43 44 45 batchsize 512
# ../results_dsn/20260603-06:07:12 1EOriginal/llama31_dsn_25_offset0.json
# ../results_dsn/20260603-06:08:29 1EOriginal/llama31_dsn_25_offset0.json
# ../results_dsn/20260603-06:10:08 1EOriginal/llama31_dsn_25_offset0.json
# ../results_dsn/20260603-06:11:04 1EOriginal/llama31_dsn_25_offset0.json
# ../results_dsn/20260603-06:12:33 1EOriginal/llama31_dsn_25_offset0.json


file_list=(
    '../results_dsn/20260603-06:10:08 1EOriginal/llama31_dsn_25_offset0.json'
)

for file_path in "${file_list[@]}"
do

    # evaluate upon the AdvBench dataset
    python -u ../evaluate_last_step.py \
        --config="../configs/transfer_${model}.py" \
        --config.train_data="../../data/AdvBench_harmful_behaviors.csv" \
        --config.data_offset=0 \
        --config.n_train_data=25 \
        --config.n_test_data=100 \
        --config.use_empty_system_prompt=False \
        --config.eval_batchsize=25 \
        --config.eval_max_new_len=512 \
        --config.eval_target_folder_name="" \
        --config.logfile="${file_path}" \
        --config.random_seed_for_sampling_targets=43 \
        --config.dsn_notes="For the last step, by generating 512 tokens, eval DSN by Refusal Matching...log file path is ${file_path}"

    # evaluate upon the JailbreakBench dataset
    python -u ../evaluate_last_step.py \
        --config="../configs/transfer_${model}.py" \
        --config.train_data="../../data/JailbreakBench_harmful_behaviors.csv" \
        --config.data_offset=0 \
        --config.n_train_data=100 \
        --config.n_test_data=0 \
        --config.use_empty_system_prompt=False \
        --config.eval_batchsize=25 \
        --config.eval_max_new_len=512 \
        --config.eval_target_folder_name="evalJBBLastStep" \
        --config.logfile="${file_path}" \
        --config.random_seed_for_sampling_targets=43 \
        --config.dsn_notes="For the last step, by generating 512 tokens, eval DSN by Refusal Matching...log file path is ${file_path}"

done
