# Addressing the Variability of Suffix-based Jailbreak Attacks

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository is forked from the official repository from [`Don't Say No: Jailbreaking LLM by Suppressing Refusal`](https://arxiv.org/abs/2404.16369)

In this work, we examine the factors that might determine the stability and effectiveness of an optimization-based jailbreak attack. Specifically, we examined the Don’t Say No (DSN) method under the influence of multiple evaluators, LLM decoding methods, and optimization objective modifications. Below, we provide instructions on how we conducted the experiments in our research. 

## Installation
The installation process is the same as the original repository of DSN (Zhou et al., 2025):

"Run the following command at the root of this repository to install the essential independencies.

```bash
pip install -e .
python -m spacy download en_core_web_sm
```
Note that we have chosen a different `transformers` version from the default `GCG` implementation, which might introduce subtle difference in Llama-2 model conversation prompt formatting. To faithfully reproduce all the results reported in the paper, e.g. both [`DSN`](https://arxiv.org/abs/2404.16369) and [`GCG`](https://arxiv.org/abs/2307.15043) attack results upon Llama-2 model, try install the `transformers` package with version 4.28.1 and `fschat` package with version 0.2.20. Both version of conda environmnets are supported by our implementation."

## Training DSN
```bash
cd /DSN/experiments/launch_scripts
bash run_dsn_attack.sh
```
To train DSN with a specific target model, set the `model` variable in `run_dsn_attack.sh` accordingly. To train DSN without any seeds set `--config.random_seed_for_sampling_targets` to -1 and to train DSN with seeds, set `--config.random_seed_for_sampling_targets` to seeds 41-45 respectively. The final .txt, .json, .pth files will be stored under the `/DSN/experiments/results_dsn` folder.

## Training GCG
```bash
cd /DSN/experiments/launch_scripts
bash run_gcg_attack.sh
```
Similarly, to train GCG with a specific target model, set the `model` variable in `run_gcg_attack.sh` accordingly. To train GCG without any seeds set `--config.random_seed_for_sampling_targets` to -1 and to train GCG with seeds, set `--config.random_seed_for_sampling_targets` to seeds 41-45 respectively. The final .txt, .json, .pth files will be stored under the `/DSN/experiments/results_dsn` folder.

## Evaluating DSN or GCG
# Refusal Matching and Refusal Classifier evaluation
To evaluate DSN or GCG, the following file first has to be run: 
```bash
cd /DSN/experiments/eval_scripts
bash lastStep_eval.sh
```
This files generates all responses from the target LLM when applying the adversarial prompt with suffix, and evaluates the responses with the Refusing Matching or Refusal Classifier evaluation method. To run this file on a specific trained suffix, place the path of its corresponding .json file from the `/DSN/experiments/results_dsn` folder inside the `file_list` variable from  the `lastStep_eval.sh` file. To evaluate with the Refusal Matching method, uncomment its original code in the `EvaluateAttack()` class from the `DSN/llm_attacks/base/attack_manager.py` file and comment out the current code for the Refusal Classifier method. Additionally, to run the evaluation on a specific target model, set the `model` variable in `lastStep_eval.sh` and the `_MODELS` variable in `/DSN/experiments/evaluate_last_step.py` accordingly. Finally, to use random seeds during evaluation, set the desired seed in the `--config.random_seed_for_sampling_targets` flag. 

After executing the `lastStep_eval.sh` file, the .json file for the AdvBench dataset is saved under the `/DSN/experiments/evalLastStep` folder and the .json file for the JailbreakBench dataset is saved under the `/DSN/experiments/evalJBBLastStep` folder.

# HarmBench and Gemma 4 evaluation
For HarmBench and Gemma 4, install the following environment: 
```bash
conda env create -f environment_gemma.yml
conda activate gemma4_gpu_env

pip uninstall -y torch torchvision torchaudio
pip install --pre torch torchvision torchaudio  --index-url https://download.pytorch.org/whl/nightly/cu121
```

To evaluate HarmBench and Gemma 4 (only possible if the `lastStep_eval.sh` file was first executed), run the following file:
```bash
cd /DSN/eval_ensemble_src
bash launch_harmbench_eval.sh
```
To evaluate on both Advbench and JailbreakBench, obtain the paths to the .json files from the `/DSN/experiments/evalLastStep` and  `/DSN/experiments/evalJBBLastStep` folders respectively and place either of them inside the `STRING_ARRAY` variable. Then, set the `random_seed` and `UseJBB` flags accordingly. 

## Various LLM Decoding Methods
To evaluate DSN under various LLM decoding methods, we set num_beams in the `EvaluateAttack()` class from `DSN/llm_attacks/base/attack_manager.py`. Specifically, we first set num_beams to 1 (Greedy), 3, 5, 7, or 9 and then evaluate DSN or GCG using `lastStep_eval.sh` and `launch_harmbench_eval.sh`. 

## Beam Search Comparisons
After obtaining all the evaluation output files for the Sampling, Greedy, and Beam=9 case, we calculated how many of the rejected prompt in the Beam=9 case, were actually accepted in the Greedy or Sampling cases. This was done by running the following file: 

```bash
cd DSN
python additional_beamsearch_experiment.py
```
Before running this file, place the right path to the corresponding output files for the Refusal Classifier, HarmBench, and Gemma 4 evaluators. 

## Greedy and Sampling Similarity Prompts
To examine how many of the accepted prompts from the Greedy case were identical to the accepted prompts from the Sampling case, we executed the following file: 

```bash
cd DSN
python beam1_sampling_similarity_prompts.py
```
Note, the beam1 and sampling .txt files were obtained by copying the printed output of `additional_beamsearch_experiment.py` to .txt files. The printed scores with the titles are, however, not included in this .txt file. 

## Case study on beam candidates
To conduct the case study on beam candidates, we set num_return_sequences in the `EvaluateAttack()` class from `DSN/llm_attacks/base/attack_manager.py`, and uncomment all the beam candidates codes accordingly.

## Refusal Keyword List Adaptations
To train DSN with different refusal keyword lists, we modified `DSN/experiments/main.py` first before running `run_dsn_attack.sh`. Speciffically, to 
utilize the doubled refusal list, tripled refusal list, halved refusal list, or curated refusal list, uncomment the lists in `DSN/experiments/main.py` respectively. 

## Window Aggregation and Filtering
For the refusal loss modifications, uncomment one of the the code for the top-k aggregation, max aggregation, variance filtering or entropy filtering in the `dsn_refusal_loss()` function from `DSN/llm_attacks/base/attack_manager.py` before training DSN with `run_dsn_attack.sh`. 

## Integration of MAGIC
To include MAGIC's contribution, exchange the current `sample_control()` funtion for the commented `sample_control()` funtion of MAGIC in `/DSN/llm_attacks/dsn/dsn_attack.py`. Afterwards, train DSN with `run_dsn_attack.sh`.

## Experiment Figures
The plotted figures for the "Various LLM Decoding Methods", "Refusal Keyword List Adaptations", and "Window Aggregation and Filtering" experiments are displayed in `/DSN/experiment_plots_final.ipynb`.

## Citation
To cite DSN's original paper, you can use: 

```bibtex
@misc{zhou2024dontsaynojailbreaking,
      title={Don't Say No: Jailbreaking LLM by Suppressing Refusal}, 
      author={Yukai Zhou and Wenjie Wang},
      year={2024},
      eprint={2404.16369},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2404.16369}, 
}
```

## Acknowledgment
The original `DSN` attack implementation is built upon modifying the `GCG` implementaion from [GCG github repo](https://github.com/llm-attacks/llm-attacks)

## License
The original `DSN` github repository is licensed under the terms of the MIT license. 