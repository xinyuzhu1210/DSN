#!/bin/bash

# sample file path
# ../experiments/evalLastStep/20260127-03:30:44 1E0/llama31_dsn_25_offset0.json
# ../experiments/evalLastStep/20260127-14:25:13 1E0/llama31_dsn_25_offset0.json
# ../experiments/evalLastStep/20260128-01:18:36 1E0/llama31_dsn_25_offset0.json
# ../experiments/evalLastStep/20260128-13:47:22 1E0/llama31_dsn_25_offset0.json
STRING_ARRAY=(
    '../experiments/evalLastStep/20260128-13:47:22 1E0/llama31_dsn_25_offset0.json'
)

for STR in "${STRING_ARRAY[@]}"; do
  python harmbench_only_evaluation.py -1 "$STR" False
done                              # random_seed, logfile, UseJBB