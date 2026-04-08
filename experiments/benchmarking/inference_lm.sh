#!/bin/bash

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json \
#         -o experiments/outputs/gpt-5.2 \
#         -m gpt-5.2 \
#         --enable-thinking-effort "medium" \
#         --resume-from-path experiments/outputs/gpt-5.2/chgk_en_benchmark_eval_reasoning_model_en_s0_gpt-5.2_20260311_182251.json

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0.json \
#         -o experiments/outputs/gpt-5.2 \
#         -m gpt-5.2

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_cot_answer_en_s0.json \
#         -o experiments/outputs/gpt-4.1 \
#         -m gpt-4.1

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_cot_answer_en_s0.json \
#         -o experiments/outputs/gpt-4.1-mini \
#         -m gpt-4.1-mini

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_cot_answer_ru_en_s0.json \
#         -o experiments/outputs/gpt-4.1 \
#         -m gpt-4.1

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_cot_answer_ru_en_s0.json \
#         -o experiments/outputs/gpt-4.1-mini \
#         -m gpt-4.1-mini

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json \
#         -o experiments/outputs/gemini-2.5-pro \
#         -m gemini-2.5-pro

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0.json \
#         -o experiments/outputs/gemini-2.5-pro \
#         -m gemini-2.5-pro

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json \
#         -o experiments/outputs/gemini-3-flash-preview \
#         -m gemini-3-flash-preview \
#         --enable-thinking-summary \
#         --enable-thinking-effort "medium"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0.json \
#         -o experiments/outputs/gemini-3-flash-preview \
#         -m gemini-3-flash-preview \
#         --enable-thinking-summary \
#         --enable-thinking-effort "medium"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json \
#         -o experiments/outputs/gemini-3-flash-preview \
#         -m gemini-3-flash-preview \
#         --enable-thinking-summary \
#         --enable-thinking-effort "minimal"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0.json \
#         -o experiments/outputs/gemini-3-flash-preview \
#         -m gemini-3-flash-preview \
#         --enable-thinking-summary \
#         --enable-thinking-effort "minimal"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json \
#         -o experiments/outputs/gemini-3.1-pro-preview \
#         -m gemini-3.1-pro-preview \
#         --enable-thinking-summary \
#         --enable-thinking-effort "medium"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0.json \
#         -o experiments/outputs/gemini-3.1-pro-preview  \
#         -m gemini-3.1-pro-preview \
#         --enable-thinking-summary \
#         --enable-thinking-effort "medium"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json \
#         -o experiments/outputs/gpt-5.4 \
#         -m gpt-5.4 \
#         --enable-thinking-summary \
#         --enable-thinking-effort "medium"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0.json \
#         -o experiments/outputs/gpt-5.4 \
#         -m gpt-5.4 \
#         --enable-thinking-summary \
#         --enable-thinking-effort "medium" \
#         --resume-from-path experiments/outputs/gpt-5.4/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0_gpt-5.4_20260313_133425.json

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0.json \
#         -o experiments/outputs/gpt-5.4 \
#         -m gpt-5.4

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json \
#         -o experiments/outputs/claude-opus-4-6 \
#         -m claude-opus-4-6 \
#         -g 16000 \
#         --enable-thinking-summary \
#         --enable-thinking-effort "medium"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_cot_answer_en_s0.json \
#         -o experiments/outputs/qwen3.5-397b-a17b \
#         -m "Qwen/Qwen3.5-397B-A17B" \
#         -g 32000 \
#         --resume-from-path experiments/outputs/qwen3.5-397b-a17b/chgk_en_benchmark_eval_cot_answer_en_s0_qwen3.5-397b-a17b_20260312_184220.json

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_cot_answer_ru_en_s0.json \
#         -o experiments/outputs/qwen3.5-397b-a17b \
#         -m "Qwen/Qwen3.5-397B-A17B" \
#         -g 32000 \
#         --resume-from-path experiments/outputs/qwen3.5-397b-a17b/chgk_ru_benchmark_eval_cot_answer_ru_en_s0_qwen3.5-397b-a17b_20260313_190040.json

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_cot_answer_en_s0.json \
#         -o experiments/outputs/llama-3.3-70b-instruct \
#         -m "meta-llama/Llama-3.3-70B-Instruct" \
#         -g 16000 \
#         --resume-from-path experiments/outputs/llama-3.3-70b-instruct/chgk_en_benchmark_eval_cot_answer_en_s0_llama-3.3-70b-instruct_20260312_200857.json

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_cot_answer_ru_en_s0.json \
#         -o experiments/outputs/llama-3.3-70b-instruct \
#         -m "meta-llama/Llama-3.3-70B-Instruct" \
#         -g 16000 \
#         --resume-from-path experiments/outputs/llama-3.3-70b-instruct/chgk_ru_benchmark_eval_cot_answer_ru_en_s0_llama-3.3-70b-instruct_20260313_161814.json

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json  \
#         -o experiments/outputs/qwen3-235b-a22b-thinking-2507 \
#         -m "Qwen/Qwen3-235B-A22B-Thinking-2507" \
#         -g 32000 \
#         --resume-from-path experiments/outputs/qwen3-235b-a22b-thinking-2507/chgk_en_benchmark_eval_reasoning_model_en_s0_qwen3-235b-a22b-thinking-2507_20260312_203137.json

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0.json  \
#         -o experiments/outputs/qwen3-235b-a22b-thinking-2507 \
#         -m "Qwen/Qwen3-235B-A22B-Thinking-2507" \
#         -g 32000 \
#         --resume-from-path experiments/outputs/qwen3-235b-a22b-thinking-2507/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0_qwen3-235b-a22b-thinking-2507_20260314_102839.json

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json \
#         -o experiments/outputs/gemini-3.1-pro-preview \
#         -m gemini-3.1-pro-preview \
#         --enable-thinking-summary \
#         --enable-thinking-effort "high" \
#         --resume-from-path experiments/outputs/gemini-3.1-pro-preview/chgk_en_benchmark_eval_reasoning_model_en_s0_gemini-3.1-pro-preview_20260312_204451.json

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0.json \
#         -o experiments/outputs/gemini-3.1-pro-preview \
#         -m gemini-3.1-pro-preview \
#         --enable-thinking-summary \
#         --enable-thinking-effort "high" \
#         --resume-from-path experiments/outputs/gemini-3.1-pro-preview/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0_gemini-3.1-pro-preview_20260313_232947.json

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json \
#         -o experiments/outputs/gemini-3.1-pro-preview \
#         -m gemini-3.1-pro-preview \
#         --enable-thinking-summary \
#         --enable-thinking-effort "low"

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json \
#         -o experiments/outputs/glm-5 \
#         -m zai-org/GLM-5

python -m cresowlve.inference_lm \
        -d experiments/data/eval/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0.json \
        -o experiments/outputs/glm-5 \
        -m zai-org/GLM-5

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_cot_answer_en_s0.json \
#         -o experiments/outputs/olmo-2-0325-32b-instruct \
#         -m allenai/OLMo-2-0325-32B-Instruct

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_cot_answer_ru_en_s0.json \
#         -o experiments/outputs/olmo-2-0325-32b-instruct \
#         -m allenai/OLMo-2-0325-32B-Instruct

python -m cresowlve.inference_lm \
        -d experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json \
        -o experiments/outputs/kimi-k2.5 \
        -m moonshotai/Kimi-K2.5

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json \
#         -o experiments/outputs/deepseek-v3.2 \
#         -m deepseek-ai/DeepSeek-V3.2

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0.json \
#         -o experiments/outputs/deepseek-v3.2 \
#         -m deepseek-ai/DeepSeek-V3.2

python -m cresowlve.inference_lm \
        -d experiments/data/eval/chgk_en_benchmark_eval_cot_answer_en_s0.json \
        -o experiments/outputs/apertus-70b-instruct-2509 \
        -m swiss-ai/Apertus-70B-Instruct-2509

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_cot_answer_en_s0.json \
#         -o experiments/outputs/qwen3-235b-a22b-instruct-2507 \
#         -m "Qwen/Qwen3-235B-A22B-Instruct-2507" \
#         -g 32000

python -m cresowlve.inference_lm \
        -d experiments/data/eval/chgk_ru_benchmark_eval_cot_answer_ru_en_s0.json \
        -o experiments/outputs/qwen3-235b-a22b-instruct-2507 \
        -m "Qwen/Qwen3-235B-A22B-Instruct-2507" \
        -g 32000

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_reasoning_model_en_s0.json \
#         -o experiments/outputs/qwen3.5-397b-a17b \
#         -m "Qwen/Qwen3.5-397B-A17B" \
#         -g 32000 \
#         --resume-from-path experiments/outputs/qwen3.5-397b-a17b/chgk_en_benchmark_eval_reasoning_model_en_s0_qwen3.5-397b-a17b_20260316_150440.json

python -m cresowlve.inference_lm \
        -d experiments/data/eval/chgk_ru_benchmark_eval_reasoning_model_ru_en_s0.json \
        -o experiments/outputs/qwen3.5-397b-a17b \
        -m "Qwen/Qwen3.5-397B-A17B" \
        -g 32000

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_cot_answer_en_s0.json \
#         -o experiments/outputs/mistral-large-3-675b-instruct-2512 \
#         -m "mistralai/Mistral-Large-3-675B-Instruct-2512" \
#         -g 32000

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_ru_benchmark_eval_cot_answer_ru_en_s0.json \
#         -o experiments/outputs/mistral-large-3-675b-instruct-2512 \
#         -m "mistralai/Mistral-Large-3-675B-Instruct-2512" \
#         -g 32000

# python -m cresowlve.inference_lm \
#         -d experiments/data/eval/chgk_en_benchmark_eval_cot_answer_en_s0.json \
#         -o experiments/outputs/c4ai-command-a-03-2025 \
#         -m "CohereLabs/c4ai-command-a-03-2025" \
#         -g 32000

python -m cresowlve.inference_lm \
        -d experiments/data/eval/chgk_ru_benchmark_eval_cot_answer_ru_en_s0.json \
        -o experiments/outputs/c4ai-command-a-03-2025 \
        -m "CohereLabs/c4ai-command-a-03-2025" \
        -g 32000