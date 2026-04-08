#!/bin/bash

# prepare source task data
python -m cresowlve.prepare_task_data \
        -i data/chgk \
        -t chgk \
        -o experiments/data/task/chgk.json