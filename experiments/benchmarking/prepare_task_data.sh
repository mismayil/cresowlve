#!/bin/bash

# prepare en benchmark task data
python -m cresowlve.prepare_task_data \
        -i experiments/data/task/chgk_benchmark.json \
        -t chgk_en_benchmark \
        -o experiments/data/task/chgk_en_benchmark.json

# prepare ru benchmark task data
python -m cresowlve.prepare_task_data \
        -i experiments/data/task/chgk_benchmark.json \
        -t chgk_ru_benchmark \
        -o experiments/data/task/chgk_ru_benchmark.json