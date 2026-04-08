#!/bin/bash

# prepare task data without external material
python -m cresowlve.prepare_task_data \
        -i experiments/outputs/gpt-4o/chgk_eval_ext_mat_annot_s0_gpt-4o_20260213_202532.json \
        -t chgk_no_external_mat \
        -o experiments/data/task/chgk_no_external_mat.json