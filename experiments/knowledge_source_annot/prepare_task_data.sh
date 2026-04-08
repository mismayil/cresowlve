#!/bin/bash

# prepare source task data
python -m cresowlve.prepare_task_data \
        -i experiments/outputs/gpt-4o/chgk_en_benchmark_eval_knowledge_source_annot_s5_gpt-4o_20260303_111851.json \
        -t chgk_benchmark_knowledge_source \
        -o experiments/data/task/chgk_benchmark_knowledge_source.json