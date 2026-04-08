#!/bin/bash

python -m cresowlve.prepare_eval_data \
        -d experiments/data/task/chgk_en_benchmark.json \
        -t knowledge_source_annot \
        -o experiments/data/eval \
        --source-datapaths experiments/data/task/chgk_en_benchmark.json \
        --shot-path experiments/knowledge_source_annot/shots.json \
        --answer-fields "source"