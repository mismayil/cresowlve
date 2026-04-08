#!/bin/bash

# python -m cresowlve.compute_metrics \
#         -d experiments/data/task/chgk_benchmark_domain.json \
#         -m domain_semdis

python -m cresowlve.compute_metrics \
        -d experiments/data/task/chgk_benchmark_domain.json \
        -m max_domain_semdis