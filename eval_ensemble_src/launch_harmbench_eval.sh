#!/bin/bash

# sample file path
# llama31
# ../experiments/evalLastStep/20260127-03:30:44 1E0/llama31_dsn_25_offset0.json
# ../experiments/evalLastStep/20260127-14:25:13 1E0/llama31_dsn_25_offset0.json
# ../experiments/evalLastStep/20260128-01:18:36 1E0/llama31_dsn_25_offset0.json
# ../experiments/evalLastStep/20260128-13:47:22 1E0/llama31_dsn_25_offset0.json
# -JBB llama31 --> JBB True
# ../experiments/evalJBBLastStep/20260127-03:30:44 1E0/llama31_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260127-14:25:13 1E0/llama31_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260128-01:18:36 1E0/llama31_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260128-13:47:22 1E0/llama31_dsn_25_offset0.json
# qwen
# ../experiments/evalLastStep/20260203-02:01:22 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260203-02:04:40 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260203-02:06:12 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260203-02:07:25 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260203-02:09:25 1E0/qwen_dsn_25_offset0.json
# -JBB qwen --> JBB True
# ../experiments/evalJBBLastStep/20260203-02:01:22 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260203-02:04:40 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260203-02:06:12 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260203-02:07:25 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260203-02:09:25 1E0/qwen_dsn_25_offset0.json
# llama3
# ../experiments/evalLastStep/20260203-20:01:23 1E0/llama3_dsn_25_offset0.json
# ../experiments/evalLastStep/20260203-20:05:44 1E0/llama3_dsn_25_offset0.json
# ../experiments/evalLastStep/20260203-20:07:35 1E0/llama3_dsn_25_offset0.json
# ../experiments/evalLastStep/20260203-20:09:50 1E0/llama3_dsn_25_offset0.json
# ../experiments/evalLastStep/20260203-20:11:07 1E0/llama3_dsn_25_offset0.json
# -JBB llama3 --> JBB True
# ../experiments/evalJBBLastStep/20260203-20:01:23 1E0/llama3_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260203-20:05:44 1E0/llama3_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260203-20:07:35 1E0/llama3_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260203-20:09:50 1E0/llama3_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260203-20:11:07 1E0/llama3_dsn_25_offset0.json

STRING_ARRAY=(
    '../experiments/evalJBBLastStep/20260203-20:01:23 1E0/llama3_dsn_25_offset0.json'
    '../experiments/evalJBBLastStep/20260203-20:05:44 1E0/llama3_dsn_25_offset0.json'
    '../experiments/evalJBBLastStep/20260203-20:07:35 1E0/llama3_dsn_25_offset0.json'
    '../experiments/evalJBBLastStep/20260203-20:09:50 1E0/llama3_dsn_25_offset0.json'
    '../experiments/evalJBBLastStep/20260203-20:11:07 1E0/llama3_dsn_25_offset0.json'
)

for STR in "${STRING_ARRAY[@]}"; do
  python harmbench_only_evaluation.py -1 "$STR" False
done                              # random_seed, logfile, UseJBB