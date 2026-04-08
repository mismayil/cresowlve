#!/bin/bash

python -m cresowlve.prepare_eval_data \
        -d experiments/data/task/chgk_en_benchmark.json \
        -t cot_answer_en \
        -o experiments/data/eval

python -m cresowlve.prepare_eval_data \
        -d experiments/data/task/chgk_ru_benchmark.json \
        -t cot_answer_ru_en \
        -o experiments/data/eval

python -m cresowlve.prepare_eval_data \
        -d experiments/data/task/chgk_en_benchmark.json \
        -t reasoning_model_en \
        -o experiments/data/eval

python -m cresowlve.prepare_eval_data \
        -d experiments/data/task/chgk_ru_benchmark.json \
        -t reasoning_model_ru_en \
        -o experiments/data/eval

python -m cresowlve.prepare_eval_data \
        -d experiments/data/task/chgk_en_benchmark.json \
        -t cot_only_final_answer_en \
        -o experiments/data/eval

python -m cresowlve.prepare_eval_data \
        -d experiments/data/task/chgk_ru_benchmark.json \
        -t cot_only_final_answer_ru_en \
        -o experiments/data/eval