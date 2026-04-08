#!/bin/bash

python -m cresowlve.compute_metrics \
        -d experiments/outputs/gpt-4o/gemini_3_flash_preview_en0_error_samples_eval_error_annot_s7_gpt-4o_20260311_151357.json \
        -m usage_and_cost \
        --source-datapath experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json