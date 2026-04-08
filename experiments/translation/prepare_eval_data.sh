#!/bin/bash

python -m cresowlve.prepare_eval_data \
        -d experiments/data/task/chgk_no_external_mat.json \
        -t translate_puzzle_ru_to_en \
        -o experiments/data/eval \
        --source-datapath experiments/data/task/chgk.json