#!/bin/bash

# prepare source task data
python -m cresowlve.prepare_task_data \
        -i experiments/outputs/gpt-4o/chgk_en_benchmark_eval_reasoning_type_annot_s5_gpt-4o_20260312_125254.json \
        -t chgk_benchmark_reasoning_types \
        -o experiments/data/task/chgk_benchmark_reasoning_types.json