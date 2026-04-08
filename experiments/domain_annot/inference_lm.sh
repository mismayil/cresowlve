#!/bin/bash

python -m cresowlve.inference_lm \
        -d experiments/data/eval/chgk_en_benchmark_eval_domain_annot_s1.json \
        -o experiments/outputs/gpt-4o \
        -m gpt-4o \
        -b 16 \
        -t 0