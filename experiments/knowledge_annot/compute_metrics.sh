#!/bin/bash

python -m cresowlve.compute_metrics \
        -d experiments/data/task/chgk_benchmark_knowledge.json \
        -m knowledge_semdis

python -m cresowlve.compute_metrics \
        -d experiments/data/task/chgk_benchmark_knowledge.json \
        -m max_knowledge_semdis