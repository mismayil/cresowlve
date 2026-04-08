#!/bin/bash

python -m cresowlve.prepare_task_data \
        -i experiments/outputs/gpt-4o/chgk_no_external_mat_eval_translate_puzzle_ru_to_en_s0_gpt-4o_20260216_121736.json \
        -t chgk_translated \
        -o experiments/data/task/chgk_no_external_mat_translated.json