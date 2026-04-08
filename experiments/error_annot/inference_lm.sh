#!/bin/bash

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/gemini_3_flash_preview_en0_error_samples_eval_error_annot_s7.json \
#         -o experiments/outputs/gpt-4o \
#         -m gpt-4o \
#         -b 16 \
#         -t 0

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/gemini_3_flash_preview_en0_error_samples_eval_error_annot_s7_shuffled.json \
#         -o experiments/outputs/gpt-4o \
#         -m gpt-4o \
#         -b 16 \
#         -t 0

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/gemini_3.1_pro_preview_en0_error_samples_eval_error_annot_s7.json \
#         -o experiments/outputs/gpt-4o \
#         -m gpt-4o \
#         -b 16 \
#         -t 0

python -m cresowlve.inference_lm \
        -d experiments/data/eval/gpt_5.4_en0_error_samples_eval_error_annot_s7.json \
        -o experiments/outputs/gpt-4o \
        -m gpt-4o \
        -b 16 \
        -t 0

python -m cresowlve.inference_lm \
        -d experiments/data/eval/deepseek_v3.2_en0_error_samples_eval_error_annot_s7.json \
        -o experiments/outputs/gpt-4o \
        -m gpt-4o \
        -b 16 \
        -t 0

python -m cresowlve.inference_lm \
        -d experiments/data/eval/gpt_4.1_en0_error_samples_eval_error_annot_s7.json \
        -o experiments/outputs/gpt-4o \
        -m gpt-4o \
        -b 16 \
        -t 0