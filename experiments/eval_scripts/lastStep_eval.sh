#!/bin/bash

export n=25
export model=qwen # choose from: gemma, gemma2, llama2, llama2_13b, llama3, llama31, mistralv02, mistralv03, qwen, vicuna_13b, vicuna

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

file_list=(
    '../results_dsn/20260209-23:12:54 1E0/qwen_dsn_25_offset0.json'
    '../results_dsn/20260210-15:16:19 1E0/qwen_dsn_25_offset0.json'
    '../results_dsn/20260210-14:50:10 1E0/qwen_dsn_25_offset0.json'
    '../results_dsn/20260210-15:06:41 1E0/qwen_dsn_25_offset0.json'
    '../results_dsn/20260210-15:08:15 1E0/qwen_dsn_25_offset0.json'
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
        --config.dsn_notes="For the last step, by generating 512 tokens, eval DSN by Refusal Matching...log file path is ${file_path}"

done
