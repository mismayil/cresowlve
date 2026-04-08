#!/bin/bash

python -m cresowlve.inference_lm \
        -d experiments/data/eval/chgk_eval_ext_mat_annot_s0.json \
        -o experiments/outputs/gpt-4o \
        -m gpt-4o \
        -b 16 \
        -t 0