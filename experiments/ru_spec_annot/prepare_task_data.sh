#!/bin/bash

# prepare russian specific annotation task data
# python -m cresowlve.prepare_task_data \
#         -i experiments/outputs/gpt-4o/chgk_no_external_mat_translated_eval_ru_spec_annot_s4_gpt-4o_20260217_064449.json \
#         -t chgk_ru_specific_annot \
#         -o experiments/data/task/chgk_no_ext_mat_ru_spec_annot.json

# prepare russian specific filtered task data
python -m cresowlve.prepare_task_data \
        -i experiments/data/task/chgk_no_ext_mat_ru_spec_annot.json \
        -t chgk_ru_spec_filtered \
        -o experiments/data/task/chgk_no_ext_mat_ru_spec_fltrd.json