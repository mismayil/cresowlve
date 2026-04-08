#!/bin/bash

# python -m cresowlve.compute_metrics \
#         -d experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_eval_data_contamination_general_en_s0_gemini-3.1-pro-preview_20260313_131224.json \
#            experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_eval_data_contamination_guided_en_s0_gemini-3.1-pro-preview_20260313_185423.json \
#         -m benchmark_contamination \
#         --source-datapath experiments/data/task/chgk_benchmark_contamination_gemini_3.1_pro_preview.json

# python -m cresowlve.compute_metrics \
#         -d experiments/outputs/gemini-3-flash-preview/chgk_benchmark_contamination_by_en_ru_diff_eval_data_contamination_general_en_s0_gemini-3-flash-preview_20260316_162854.json \
#            experiments/outputs/gemini-3-flash-preview/chgk_benchmark_contamination_by_en_ru_diff_eval_data_contamination_guided_en_s0_gemini-3-flash-preview_20260316_163009.json \
#         -m benchmark_contamination \
#         --source-datapath experiments/data/task/chgk_benchmark_contamination_by_en_ru_diff_gemini_3_flash_preview.json

# python -m cresowlve.compute_metrics \
#         -d experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_by_en_ru_diff_gemini_3.1_pro_preview_eval_data_contamination_general_en_s0_gemini-3.1-pro-preview_20260316_173536.json \
#            experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_by_en_ru_diff_gemini_3.1_pro_preview_eval_data_contamination_guided_en_s0_gemini-3.1-pro-preview_20260316_174952.json \
#         -m benchmark_contamination \
#         --source-datapath experiments/data/task/chgk_benchmark_contamination_by_en_ru_diff_gemini_3.1_pro_preview.json

# python -m cresowlve.compute_metrics \
#         -d experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_quiz_annot_gemini_3.1_pro_preview_eval_data_contamination_quiz_mcq_s0_gemini-3.1-pro-preview_20260316_231240.json \
#         -m benchmark_contamination_by_quiz_mcq \
#         --source-datapath experiments/data/task/chgk_benchmark_contamination_quiz_annot_gemini_3.1_pro_preview.json

# python -m cresowlve.compute_metrics \
#         -d experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_quiz_bdq_gemini_3.1_pro_preview_eval_data_contamination_quiz_bdq_s0_gemini-3.1-pro-preview_20260317_000611.json \
#         -m benchmark_contamination_quiz_bdq_pos_bias

# python -m cresowlve.compute_metrics \
#         -d experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_quiz_bcq1_gemini_3.1_pro_preview_eval_data_contamination_quiz_bcq_s0_gemini-3.1-pro-preview_20260317_004107.json \
#         -m benchmark_contamination_by_quiz_mcq \
#         --source-datapath experiments/data/task/chgk_benchmark_contamination_quiz_bcq1_gemini_3.1_pro_preview.json

python -m cresowlve.compute_metrics \
        -d experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_quiz_bcq2_gemini_3.1_pro_preview_eval_data_contamination_quiz_bcq_s0_gemini-3.1-pro-preview_20260321_182158.json \
        -m benchmark_contamination_by_quiz_mcq \
        --source-datapath experiments/data/task/chgk_benchmark_contamination_quiz_bcq2_gemini_3.1_pro_preview.json

python -m cresowlve.compute_metrics \
        -d experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_quiz_bcq3_gemini_3.1_pro_preview_eval_data_contamination_quiz_bcq_s0_gemini-3.1-pro-preview_20260321_182749.json \
        -m benchmark_contamination_by_quiz_mcq \
        --source-datapath experiments/data/task/chgk_benchmark_contamination_quiz_bcq3_gemini_3.1_pro_preview.json

# python -m cresowlve.compute_metrics \
#         -d experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_quiz_ctrl_bcq1_gemini_3.1_pro_preview_eval_data_contamination_quiz_bcq_s0_gemini-3.1-pro-preview_20260317_134148.json \
#         -m benchmark_contamination_by_quiz_mcq \
#         --source-datapath experiments/data/task/chgk_benchmark_contamination_quiz_ctrl_bcq1_gemini_3.1_pro_preview.json