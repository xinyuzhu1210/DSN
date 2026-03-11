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
# qwen batch_size 41, 42, 43, 44, 45, aug_sampling = false
# ../experiments/evalLastStep/20260206-17:12:43 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260209-19:52:54 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260209-19:56:48 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260209-19:58:46 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260209-20:22:30 1E0/qwen_dsn_25_offset0.json
# qwen batch_size 41, 42, 43, 44, 45, aug_sampling = false, --> JBB True
# ../experiments/evalJBBLastStep/20260206-17:12:43 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260209-19:52:54 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260209-19:56:48 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260209-19:58:46 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260209-20:22:30 1E0/qwen_dsn_25_offset0.json
# qwen batch_size 41, 42, 43, 44, 45, aug_sampling = true
# ../experiments/evalLastStep/20260209-23:12:54 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260210-15:16:19 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260210-14:50:10 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260210-15:06:41 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260210-15:08:15 1E0/qwen_dsn_25_offset0.json
# qwen batch_size 41, 42, 43, 44, 45, aug_sampling = true, --> JBB True
# ../experiments/evalJBBLastStep/20260209-23:12:54 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260210-15:16:19 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260210-14:50:10 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260210-15:06:41 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260210-15:08:15 1E0/qwen_dsn_25_offset0.json
# Qwen2-7B batch size 256, seed 41, 42, 43, 44, 45, use_aug_sampling=False, topk=10
# ../experiments/evalLastStep/20260214-00:37:15 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260214-00:39:58 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260214-00:41:13 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260214-00:42:30 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260214-00:43:43 1E0/qwen_dsn_25_offset0.json
# Qwen2-7B batch size 256, seed 41, 42, 43, 44, 45, use_aug_sampling=False, topk=10 --> JBB True
# ../experiments/evalJBBLastStep/20260214-00:37:15 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260214-00:39:58 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260214-00:41:13 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260214-00:42:30 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260214-00:43:43 1E0/qwen_dsn_25_offset0.json
# Qwen2-7B train, batch size 256, seed 41, 42, 43, 44, 45, use_aug_sampling=False, doubled prefixes list
# ../experiments/evalLastStep/20260214-01:14:28 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260214-01:17:29 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260214-01:18:57 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260214-01:20:00 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260216-18:34:40 1E0/qwen_dsn_25_offset0.json
# Qwen2-7B train, batch size 256, seed 41, 42, 43, 44, 45, use_aug_sampling=False, doubled prefixes list --> JBB True
# ../experiments/evalJBBLastStep/20260214-01:14:28 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260214-01:17:29 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260214-01:18:57 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260214-01:20:00 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260216-18:34:40 1E0/qwen_dsn_25_offset0.json
# Qwen2-7B train, batch size 256, seed 41, 42, 43, 44, 45, use_aug_sampling=False, Magic integration
# ../experiments/evalLastStep/20260311-04:27:52 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260311-04:30:23 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260311-04:33:09 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260311-04:35:24 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalLastStep/20260311-04:36:33 1E0/qwen_dsn_25_offset0.json
# Qwen2-7B train, batch size 256, seed 41, 42, 43, 44, 45, use_aug_sampling=False, Magic integration, JBB true
# ../experiments/evalJBBLastStep/20260311-04:27:52 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260311-04:30:23 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260311-04:33:09 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260311-04:35:24 1E0/qwen_dsn_25_offset0.json
# ../experiments/evalJBBLastStep/20260311-04:36:33 1E0/qwen_dsn_25_offset0.json

STRING_ARRAY=(
  '../experiments/evalJBBLastStep/20260311-04:36:33 1E0/qwen_dsn_25_offset0.json'
)

for STR in "${STRING_ARRAY[@]}"; do
  python harmbench_only_evaluation.py 45 "$STR" True
done                              # random_seed, logfile, UseJBB