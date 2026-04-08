#!/bin/bash

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gpt-4o/gemini_3_flash_preview_en0_error_samples_eval_error_annot_s7_gpt-4o_20260311_151357.json \
#         -t chgk_benchmark_error_annot \
#         -o experiments/data/task/chgk_benchmark_error_annot_gemini_3_flash_en0.json

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gpt-4o/gemini_3_flash_preview_en0_error_samples_eval_error_annot_s7_shuffled_gpt-4o_20260311_162800.json \
#         -t chgk_benchmark_error_annot \
#         -o experiments/data/task/chgk_benchmark_error_annot_shuffled_gemini_3_flash_en0.json

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gpt-4o/gemini_3.1_pro_preview_en0_error_samples_eval_error_annot_s7_gpt-4o_20260319_211858.json \
#         -t chgk_benchmark_error_annot \
#         -o experiments/data/task/chgk_benchmark_error_annot_gemini_3.1_pro_en0.json

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gpt-5.4/chgk_en_benchmark_eval_reasoning_model_en_s0_gpt-5.4_20260312_101028.json \
#         -t chgk_benchmark_results_error \
#         -o experiments/data/error_analysis/en0/gpt_5.4_en0_error_samples.json

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/deepseek-v3.2/chgk_en_benchmark_eval_reasoning_model_en_s0_deepseek-v3.2_20260315_133331.json \
#         -t chgk_benchmark_results_error \
#         -o experiments/data/error_analysis/en0/deepseek_v3.2_en0_error_samples.json

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gpt-4.1/chgk_en_benchmark_eval_cot_answer_en_s0_gpt-4.1_20260228_123352.json \
#         -t chgk_benchmark_results_error \
#         -o experiments/data/error_analysis/en0/gpt_4.1_en0_error_samples.json

python -m cresowlve.prepare_task_data \
        -i experiments/outputs/gpt-4o/gpt_5.4_en0_error_samples_eval_error_annot_s7_gpt-4o_20260322_113050.json \
        -t chgk_benchmark_error_annot \
        -o experiments/data/task/chgk_benchmark_error_annot_gpt_5.4_en0.json

python -m cresowlve.prepare_task_data \
        -i experiments/outputs/gpt-4o/deepseek_v3.2_en0_error_samples_eval_error_annot_s7_gpt-4o_20260322_113705.json \
        -t chgk_benchmark_error_annot \
        -o experiments/data/task/chgk_benchmark_error_annot_deepseek_v3.2_en0.json

python -m cresowlve.prepare_task_data \
        -i experiments/outputs/gpt-4o/gpt_4.1_en0_error_samples_eval_error_annot_s7_gpt-4o_20260322_114425.json \
        -t chgk_benchmark_error_annot \
        -o experiments/data/task/chgk_benchmark_error_annot_gpt_4.1_en0.json