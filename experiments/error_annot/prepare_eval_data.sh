#!/bin/bash

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/error_analysis/gemini_3_flash_preview_en0_error_samples.json \
#         -t error_annot \
#         -o experiments/data/eval \
#         --source-datapaths experiments/data/task/chgk_en_benchmark.json \
#                            experiments/outputs/gemini-3-flash-preview/chgk_en_benchmark_eval_reasoning_model_en_s0_gemini-3-flash-preview_20260302_151010.json \
#         --shot-path experiments/error_annot/shots.json \
#         --answer-fields "annotation"

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/error_analysis/gemini_3_flash_preview_en0_error_samples.json \
#         -t error_annot \
#         -o experiments/data/eval \
#         --source-datapaths experiments/data/task/chgk_en_benchmark.json \
#                            experiments/outputs/gemini-3-flash-preview/chgk_en_benchmark_eval_reasoning_model_en_s0_gemini-3-flash-preview_20260302_151010.json \
#         --shot-path experiments/error_annot/shots.json \
#         --answer-fields "annotation" \
#         --shuffle-shots \
#         --suffix "_shuffled"

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/error_analysis/gemini_3.1_pro_preview_en0_error_samples.json \
#         -t error_annot \
#         -o experiments/data/eval \
#         --source-datapaths experiments/data/task/chgk_en_benchmark.json \
#                            experiments/outputs/gemini-3.1-pro-preview/chgk_en_benchmark_eval_reasoning_model_en_s0_gemini-3.1-pro-preview_20260312_204451.json \
#         --shot-path experiments/error_annot/shots.json \
#         --answer-fields "annotation" \
#         --shuffle-shots

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/error_analysis/en0/gpt_5.4_en0_error_samples.json \
#         -t error_annot \
#         -o experiments/data/eval \
#         --source-datapaths experiments/data/task/chgk_en_benchmark.json \
#                            experiments/outputs/gpt-5.4/chgk_en_benchmark_eval_reasoning_model_en_s0_gpt-5.4_20260312_101028.json \
#         --shot-path experiments/error_annot/shots.json \
#         --answer-fields "annotation" \
#         --shuffle-shots

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/error_analysis/en0/deepseek_v3.2_en0_error_samples.json \
#         -t error_annot \
#         -o experiments/data/eval \
#         --source-datapaths experiments/data/task/chgk_en_benchmark.json \
#                            experiments/outputs/deepseek-v3.2/chgk_en_benchmark_eval_reasoning_model_en_s0_deepseek-v3.2_20260315_133331.json \
#         --shot-path experiments/error_annot/shots.json \
#         --answer-fields "annotation" \
#         --shuffle-shots

python -m cresowlve.prepare_eval_data \
        -d experiments/data/error_analysis/en0/gpt_4.1_en0_error_samples.json \
        -t error_annot \
        -o experiments/data/eval \
        --source-datapaths experiments/data/task/chgk_en_benchmark.json \
                           experiments/outputs/gpt-4.1/chgk_en_benchmark_eval_cot_answer_en_s0_gpt-4.1_20260228_123352.json \
        --shot-path experiments/error_annot/shots.json \
        --answer-fields "annotation" \
        --shuffle-shots