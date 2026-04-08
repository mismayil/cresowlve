#!/bin/bash

python -m cresowlve.inference_lm \
        -d experiments/data/eval/chgk_no_external_mat_eval_translate_puzzle_ru_to_en_s0.json \
        -o experiments/outputs/gpt-4o \
        -m gpt-4o \
        -b 16 \
        -t 0