#!/bin/bash

# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gpt-4o/chgk_en_benchmark_eval_domain_annot_s1_gpt-4o_20260302_154455.json \
#         -t chgk_benchmark_domain \
#         -o experiments/data/task/chgk_benchmark_domain.json

python -m cresowlve.prepare_task_data \
        -i experiments/data/task/chgk_benchmark_domain.json \
           experiments/domain_annot/domain_mapping.json \
        -t chgk_benchmark_grouped_domain \
        -o experiments/data/task/chgk_benchmark_domain.json \
        --process-together