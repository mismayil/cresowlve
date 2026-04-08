#!/bin/bash

python -m cresowlve.prepare_eval_data \
        -d experiments/data/task/chgk_en_benchmark.json \
        -t reasoning_type_annot \
        -o experiments/data/eval \
        --source-datapaths experiments/data/task/chgk_en_benchmark.json \
        --shot-path experiments/reasoning_type_annot/shots.json \
        --shuffle-shots