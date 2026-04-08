#!/bin/bash

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gemini-3.1-pro-preview/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0_gemini-3.1-pro-preview_20260310_160621.json \
#            experiments/data/task/chgk_ru_benchmark.json \
#         -t chgk_benchmark_contamination \
#         -o experiments/data/task/chgk_benchmark_contamination_gemini_3.1_pro_preview.json \
#         --process-together

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gemini-3-flash-preview/chgk_en_benchmark_eval_reasoning_model_en_s0_gemini-3-flash-preview_20260314_131112.json \
#            experiments/outputs/gemini-3-flash-preview/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0_gemini-3-flash-preview_20260314_134946.json \
#            experiments/data/task/chgk_ru_benchmark.json \
#         -t chgk_benchmark_contamination_by_en_ru_diff \
#         -o experiments/data/task/chgk_benchmark_contamination_by_en_ru_diff_gemini_3_flash_preview.json \
#         --process-together

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gemini-3.1-pro-preview/chgk_en_benchmark_eval_reasoning_model_en_s0_gemini-3.1-pro-preview_20260314_130907.json \
#            experiments/outputs/gemini-3.1-pro-preview/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0_gemini-3.1-pro-preview_20260314_143543.json \
#            experiments/data/task/chgk_ru_benchmark.json \
#         -t chgk_benchmark_contamination_by_en_ru_diff \
#         -o experiments/data/task/chgk_benchmark_contamination_by_en_ru_diff_gemini_3.1_pro_preview.json \
#         --process-together

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gpt-4o/chgk_benchmark_contamination_by_en_ru_diff_gemini_3.1_pro_preview_eval_data_contamination_quiz_annot_s0_gpt-4o_20260316_222142.json \
#            experiments/data/task/chgk_ru_benchmark.json \
#         -t chgk_benchmark_contamination_quiz_annot \
#         -o experiments/data/task/chgk_benchmark_contamination_quiz_annot_gemini_3.1_pro_preview.json \
#         --process-together

# python -m cresowlve.prepare_task_data \
#         -i experiments/data/task/chgk_benchmark_contamination_quiz_annot_gemini_3.1_pro_preview.json \
#         -t chgk_benchmark_contamination_quiz_bdq \
#         -o experiments/data/task/chgk_benchmark_contamination_quiz_bdq_gemini_3.1_pro_preview.json \

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_quiz_bdq_gemini_3.1_pro_preview_eval_data_contamination_quiz_bdq_s0_gemini-3.1-pro-preview_20260317_000611.json \
#            experiments/data/task/chgk_benchmark_contamination_quiz_bdq_gemini_3.1_pro_preview.json \
#         -t chgk_benchmark_contamination_quiz_bcq \
#         -o experiments/data/task/chgk_benchmark_contamination_quiz_bcq1_gemini_3.1_pro_preview.json \
#          --process-together

python -m cresowlve.prepare_task_data \
        -i experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_quiz_bdq_gemini_3.1_pro_preview_eval_data_contamination_quiz_bdq_s0_gemini-3.1-pro-preview_20260317_000611.json \
           experiments/data/task/chgk_benchmark_contamination_quiz_bdq_gemini_3.1_pro_preview.json \
        -t chgk_benchmark_contamination_quiz_bcq \
        -o experiments/data/task/chgk_benchmark_contamination_quiz_bcq2_gemini_3.1_pro_preview.json \
         --process-together

python -m cresowlve.prepare_task_data \
        -i experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_quiz_bdq_gemini_3.1_pro_preview_eval_data_contamination_quiz_bdq_s0_gemini-3.1-pro-preview_20260317_000611.json \
           experiments/data/task/chgk_benchmark_contamination_quiz_bdq_gemini_3.1_pro_preview.json \
        -t chgk_benchmark_contamination_quiz_bcq \
        -o experiments/data/task/chgk_benchmark_contamination_quiz_bcq3_gemini_3.1_pro_preview.json \
         --process-together

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gemini-3.1-pro-preview/chgk_en_benchmark_eval_reasoning_model_en_s0_gemini-3.1-pro-preview_20260314_130907.json \
#            experiments/outputs/gemini-3.1-pro-preview/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0_gemini-3.1-pro-preview_20260314_143543.json \
#            experiments/data/task/chgk_ru_benchmark.json \
#         -t chgk_benchmark_contamination_control_by_en_ru_diff \
#         -o experiments/data/task/chgk_benchmark_contamination_ctrl_by_en_ru_diff_gemini_3.1_pro_preview.json \
#         --process-together

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gpt-4o/chgk_benchmark_contamination_ctrl_by_en_ru_diff_gemini_3.1_pro_preview_eval_data_contamination_quiz_annot_s0_gpt-4o_20260317_120442.json \
#            experiments/data/task/chgk_ru_benchmark.json \
#         -t chgk_benchmark_contamination_quiz_annot \
#         -o experiments/data/task/chgk_benchmark_contamination_quiz_annot_ctrl_gemini_3.1_pro_preview.json \
#         --process-together

# python -m cresowlve.prepare_task_data \
#         -i experiments/data/task/chgk_benchmark_contamination_quiz_annot_ctrl_gemini_3.1_pro_preview.json \
#         -t chgk_benchmark_contamination_quiz_bdq \
#         -o experiments/data/task/chgk_benchmark_contamination_quiz_ctrl_bdq_gemini_3.1_pro_preview.json \

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_quiz_bdq_gemini_3.1_pro_preview_eval_data_contamination_quiz_bdq_s0_gemini-3.1-pro-preview_20260317_000611.json \
#            experiments/data/task/chgk_benchmark_contamination_quiz_ctrl_bdq_gemini_3.1_pro_preview.json \
#         -t chgk_benchmark_contamination_quiz_bcq \
#         -o experiments/data/task/chgk_benchmark_contamination_quiz_ctrl_bcq1_gemini_3.1_pro_preview.json \
#          --process-together