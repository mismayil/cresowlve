#!/bin/bash

python -m cresowlve.prepare_eval_data \
        -d experiments/data/task/chgk_no_external_mat_translated.json \
        -t ru_spec_annot \
        -o experiments/data/eval \
        --source-datapaths "experiments/data/task/chgk.json" "experiments/data/task/chgk_no_external_mat_translated.json" \
        --shot-path experiments/ru_spec_annot/shots.json \
        --num-shots 4 \
        --answer-fields "shot_answer" "reasoning"