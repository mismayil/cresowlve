#!/bin/bash

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/task/chgk_benchmark_contamination_gemini_3.1_pro_preview.json \
#         -t data_contamination_guided_en \
#         -o experiments/data/eval

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/task/chgk_benchmark_contamination_gemini_3.1_pro_preview.json \
#         -t data_contamination_general_en \
#         -o experiments/data/eval

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/task/chgk_benchmark_contamination_by_en_ru_diff_gemini_3_flash_preview.json \
#         -t data_contamination_guided_en \
#         -o experiments/data/eval

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/task/chgk_benchmark_contamination_by_en_ru_diff_gemini_3_flash_preview.json \
#         -t data_contamination_general_en \
#         -o experiments/data/eval

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/task/chgk_benchmark_contamination_by_en_ru_diff_gemini_3.1_pro_preview.json \
#         -t data_contamination_guided_en \
#         -o experiments/data/eval

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/task/chgk_benchmark_contamination_by_en_ru_diff_gemini_3.1_pro_preview.json \
#         -t data_contamination_general_en \
#         -o experiments/data/eval

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/task/chgk_benchmark_contamination_by_en_ru_diff_gemini_3.1_pro_preview.json \
#         --source-datapath experiments/data/task/chgk_ru_benchmark.json \
#         -t data_contamination_quiz_annot \
#         -o experiments/data/eval

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/task/chgk_benchmark_contamination_quiz_annot_gemini_3.1_pro_preview.json \
#         -t data_contamination_quiz_mcq \
#         -o experiments/data/eval

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/task/chgk_benchmark_contamination_quiz_bdq_gemini_3.1_pro_preview.json \
#         -t data_contamination_quiz_bdq \
#         -o experiments/data/eval

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/task/chgk_benchmark_contamination_quiz_bcq1_gemini_3.1_pro_preview.json \
#         -t data_contamination_quiz_bcq \
#         -o experiments/data/eval

python -m cresowlve.prepare_eval_data \
        -d experiments/data/task/chgk_benchmark_contamination_quiz_bcq2_gemini_3.1_pro_preview.json \
        -t data_contamination_quiz_bcq \
        -o experiments/data/eval

python -m cresowlve.prepare_eval_data \
        -d experiments/data/task/chgk_benchmark_contamination_quiz_bcq3_gemini_3.1_pro_preview.json \
        -t data_contamination_quiz_bcq \
        -o experiments/data/eval

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/task/chgk_benchmark_contamination_ctrl_by_en_ru_diff_gemini_3.1_pro_preview.json \
#         --source-datapath experiments/data/task/chgk_ru_benchmark.json \
#         -t data_contamination_quiz_annot \
#         -o experiments/data/eval

# python -m cresowlve.prepare_eval_data \
#         -d experiments/data/task/chgk_benchmark_contamination_quiz_ctrl_bcq1_gemini_3.1_pro_preview.json \
#         -t data_contamination_quiz_bcq \
#         -o experiments/data/eval