#!/bin/bash

python -m cresowlve.prepare_eval_data \
        -d experiments/data/task/chgk.json \
        -t ext_mat_annot \
        -o experiments/data/eval