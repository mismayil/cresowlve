#!/bin/bash

# prepare source task data
python -m cresowlve.prepare_task_data \
        -i experiments/outputs/gpt-4o/chgk_en_benchmark_eval_knowledge_annot_s1_gpt-4o_20260228_153639.json \
        -t chgk_benchmark_knowledge \
        -o experiments/data/task/chgk_benchmark_knowledge.json