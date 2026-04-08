#!/bin/bash

python -m cresowlve.prepare_eval_data \
        -d experiments/data/task/chgk_en_benchmark.json \
        -t culture_lang_annot \
        -o experiments/data/eval \
        --source-datapaths experiments/data/task/chgk_en_benchmark.json \
        --shot-path experiments/culture_lang_annot/shots.json \
        --answer-fields "cultures"