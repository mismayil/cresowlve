#!/bin/bash

python -m cresowlve.inference_lm \
        -d experiments/data/eval/chgk_no_external_mat_translated_eval_filter_ru_specific_s4.json \
        -o experiments/outputs/gpt-4o \
        -m gpt-4o \
        -b 16 \
        -t 0