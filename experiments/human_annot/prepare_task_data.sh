#!/bin/bash

# prepare source task data
python -m cresowlve.prepare_task_data \
        -i experiments/data/human_annot \
        -t chgk_benchmark \
        -o experiments/data/task/chgk_benchmark.json \
        --process-together