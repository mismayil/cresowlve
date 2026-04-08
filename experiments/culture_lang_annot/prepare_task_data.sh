#!/bin/bash

# prepare source task data
python -m cresowlve.prepare_task_data \
        -i experiments/outputs/gpt-4o/chgk_en_benchmark_eval_culture_lang_annot_s4_gpt-4o_20260310_144116.json \
        -t chgk_benchmark_culture_lang \
        -o experiments/data/task/chgk_benchmark_culture_lang.json