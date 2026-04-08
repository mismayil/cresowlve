#!/bin/bash

python -m cresowlve.prepare_human_annot_data \
        -d experiments/data/task/chgk_no_ext_mat_ru_spec_fltrd.json \
        -o experiments/data/human_annot \
        --source-datapaths "experiments/data/task/chgk.json" "experiments/data/task/chgk_no_external_mat_translated.json" \
        --annot-fields "annot_check" "annot_comments" \
        --num-splits 3