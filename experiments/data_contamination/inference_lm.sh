#!/bin/bash

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_benchmark_contamination_eval_data_contamination_general_en_s0.json \
#         -o experiments/outputs/gemini-3.1-pro-preview \
#         -m gemini-3.1-pro-preview \
#         -b 16 \
#         -t 0

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_benchmark_contamination_eval_data_contamination_guided_en_s0.json \
#         -o experiments/outputs/gemini-3.1-pro-preview \
#         -m gemini-3.1-pro-preview \
#         -b 16 \
#         -t 0 \
#         --resume-from-path experiments/outputs/gemini-3.1-pro-preview/chgk_benchmark_contamination_eval_data_contamination_guided_en_s0_gemini-3.1-pro-preview_20260313_185423.json

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_benchmark_contamination_by_en_ru_diff_eval_data_contamination_general_en_s0.json \
#         -o experiments/outputs/gemini-3-flash-preview \
#         -m gemini-3-flash-preview \
#         -b 16 \
#         -t 0 \
#         --enable-thinking-effort "minimal"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_benchmark_contamination_by_en_ru_diff_eval_data_contamination_guided_en_s0.json \
#         -o experiments/outputs/gemini-3-flash-preview \
#         -m gemini-3-flash-preview \
#         -b 16 \
#         -t 0 \
#         --enable-thinking-effort "minimal"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_benchmark_contamination_by_en_ru_diff_gemini_3.1_pro_preview_eval_data_contamination_general_en_s0.json \
#         -o experiments/outputs/gemini-3.1-pro-preview \
#         -m gemini-3.1-pro-preview \
#         -b 16 \
#         -t 0 \
#         --enable-thinking-effort "low"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_benchmark_contamination_by_en_ru_diff_gemini_3.1_pro_preview_eval_data_contamination_guided_en_s0.json \
#         -o experiments/outputs/gemini-3.1-pro-preview \
#         -m gemini-3.1-pro-preview \
#         -b 16 \
#         -t 0 \
#         --enable-thinking-effort "low"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_benchmark_contamination_by_en_ru_diff_gemini_3.1_pro_preview_eval_data_contamination_quiz_annot_s0.json \
#         -o experiments/outputs/gpt-4o \
#         -m gpt-4o \
#         -b 16 \
#         -t 0

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_benchmark_contamination_quiz_annot_gemini_3.1_pro_preview_eval_data_contamination_quiz_mcq_s0.json \
#         -o experiments/outputs/gemini-3.1-pro-preview \
#         -m gemini-3.1-pro-preview \
#         -b 16 \
#         -t 0 \
#         --enable-thinking-effort "low"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_benchmark_contamination_quiz_bdq_gemini_3.1_pro_preview_eval_data_contamination_quiz_bdq_s0.json \
#         -o experiments/outputs/gemini-3.1-pro-preview \
#         -m gemini-3.1-pro-preview \
#         -b 16 \
#         -t 0 \
#         --enable-thinking-effort "low"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_benchmark_contamination_quiz_bcq1_gemini_3.1_pro_preview_eval_data_contamination_quiz_bcq_s0.json \
#         -o experiments/outputs/gemini-3.1-pro-preview \
#         -m gemini-3.1-pro-preview \
#         -b 16 \
#         -t 0 \
#         --enable-thinking-effort "low"

python -m cresowlve.inference_lm \
        -d experiments/data/eval/chgk_benchmark_contamination_quiz_bcq2_gemini_3.1_pro_preview_eval_data_contamination_quiz_bcq_s0.json \
        -o experiments/outputs/gemini-3.1-pro-preview \
        -m gemini-3.1-pro-preview \
        -b 16 \
        -t 0 \
        --enable-thinking-effort "low"

python -m cresowlve.inference_lm \
        -d experiments/data/eval/chgk_benchmark_contamination_quiz_bcq3_gemini_3.1_pro_preview_eval_data_contamination_quiz_bcq_s0.json \
        -o experiments/outputs/gemini-3.1-pro-preview \
        -m gemini-3.1-pro-preview \
        -b 16 \
        -t 0 \
        --enable-thinking-effort "low"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_benchmark_contamination_ctrl_by_en_ru_diff_gemini_3.1_pro_preview_eval_data_contamination_quiz_annot_s0.json \
#         -o experiments/outputs/gpt-4o \
#         -m gpt-4o \
#         -b 16 \
#         -t 0

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_benchmark_contamination_quiz_ctrl_bcq1_gemini_3.1_pro_preview_eval_data_contamination_quiz_bcq_s0.json \
#         -o experiments/outputs/gemini-3.1-pro-preview \
#         -m gemini-3.1-pro-preview \
#         -b 16 \
#         -t 0 \
#         --enable-thinking-effort "low"