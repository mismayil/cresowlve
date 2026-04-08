import re
from string import Formatter
import json
import uuid
import os
import glob
import pandas as pd
import wandb
import numpy as np

MODEL_COSTS = {
    "gpt-4": {'input': 30e-6, 'output': 60e-6},
    "gpt-4o": {'input': 2.5e-6, 'output': 10e-6},
    "gpt-4-0125-preview": {'input': 10e-6, 'output': 30e-6},
    "gpt-4o-2024-08-06": {'input': 2.5e-6, 'output': 10e-6},
    "gemini-1.5-flash": {'input': 3.5e-7, 'output': 1.05e-6},
    "gemini-1.5-pro": {'input': 3.5e-6, 'output': 10.5e-6},
    "claude-3-5-sonnet-20240620": {'input': 3e-6, 'output': 15e-6},
    "claude-3-5-haiku-20241022": {"input": 1e-6, "output": 5e-6},
    "claude-3-opus-20240229": {'input': 15e-6, 'output': 75e-6},
    "claude-3-sonnet-20240229": {'input': 3e-6, 'output': 15e-6},
    "claude-3-haiku-20240307": {'input': 0.25e-6, 'output': 1.25e-6},
    "gpt-5-mini": {'input': 0.25e-6, 'output': 2e-6},
    "gpt-5": {'input': 1.25e-6, 'output': 10e-6},
    "gpt-5.2-2025-12-11": {'input': 1.75e-6, 'output': 14e-6},
    "gpt-5.2": {'input': 1.75e-6, 'output': 14e-6},
    "gpt-5.4": {'input': 2.5e-6, 'output': 15e-6}
}

def generate_datetime_id():
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def num_tokens_from_string(text, model):
    import tiktoken
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("o200k_base")
    num_tokens = len(encoding.encode(text))
    return num_tokens

def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def read_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]
    return data

def write_json(data, path, ensure_ascii=False, indent=4):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)

def generate_unique_id():
    return str(uuid.uuid4()).split("-")[-1]

def find_files(directory, extension="json"):
    return glob.glob(f"{directory}/**/*.{extension}", recursive=True)

def concatenate(lists):
    return [item for sublist in lists for item in sublist]

def levenshtein_distance(s, t):
    m = len(s)
    n = len(t)
    d = [[0] * (n + 1) for i in range(m + 1)]  

    for i in range(1, m + 1):
        d[i][0] = i

    for j in range(1, n + 1):
        d[0][j] = j
    
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(d[i - 1][j] + 1,      # deletion
                          d[i][j - 1] + 1,      # insertion
                          d[i - 1][j - 1] + cost) # substitution   

    return d[m][n]

def batched(lst, size=4):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

def compute_usage(sample, model, 
                  input_attrs=["system_prompt", "user_prompt"], 
                  output_attrs=["output"],
                  max_input_tokens=None, max_output_tokens=None):
    if model not in MODEL_COSTS:
        return None, None

    usage = {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0
    }

    input_tokens = 0
    output_tokens = 0

    if max_input_tokens:
        input_tokens = max_input_tokens
    else:
        for attr in input_attrs:
            if attr in sample:
                input_tokens += num_tokens_from_string(sample[attr], model)

    if max_output_tokens:
        output_tokens = max_output_tokens        
    else:
        for attr in output_attrs:
            if attr in sample:
                output_tokens += num_tokens_from_string(sample[attr], model)

    usage = {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens
    }

    input_cost = usage["input_tokens"] * MODEL_COSTS[model]["input"]
    output_cost = usage["output_tokens"] * MODEL_COSTS[model]["output"]

    return usage, {
        "input": input_cost,
        "output": output_cost,
        "total": input_cost + output_cost
    }

def get_template_keys(template):
    return [i[1] for i in Formatter().parse(template) if i[1] is not None]

def is_immutable(obj):
    return isinstance(obj, (str, int, float, bool, tuple, type(None)))

def cache(cache_dict):
    def decorator_cache(func):
        def wrapper(*args, **kwargs):
            if all(is_immutable(arg) for arg in args) and all(is_immutable(val) for val in kwargs.values()):
                key = (args, frozenset(kwargs.items()))
                if key in cache_dict:
                    return cache_dict[key]
                result = func(*args, **kwargs)
                cache_dict[key] = result
            else:
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_cache

def concat_dfs(df_lst):
    shared_columns = None

    for df in df_lst:
        if shared_columns is None:
            shared_columns = set(df.columns)
        else:
            shared_columns.intersection_update(df.columns)
    
    shared_columns = list(shared_columns)
    return pd.concat([df[shared_columns] for df in df_lst])

def none_or_int(value):
    if value.lower() == "none":
        return None
    return int(value)

def none_or_str(value):
    if value.lower() == "none":
        return None
    return str(value)

def wandb_log_run(name, config=None, metrics=None, project=None, run_id=None):
    if run_id is not None:
        run = get_wandb_run(run_id, project=project)
        if run:
            run.delete()
    run = wandb.init(name=name, project=project, config=config)
    if metrics:
        run.log(metrics)
    run.finish()
    return run


def get_wandb_run(run_id, entity=None, project=None):
    entity = os.getenv("WANDB_ENTITY") if entity is None else entity
    project = os.getenv("WANDB_PROJECT") if project is None else project
    try:
        return wandb.Api().run(f"{entity}/{project}/{run_id}")
    except Exception as e:
        print(f"Error getting run {run_id}: {str(e)}")
        return None
    
def prepare_metrics_for_wandb(metrics, exclude_prefixes=None):
    if exclude_prefixes is None:
        exclude_prefixes = []

    wandb_metrics = {}

    for key, value in metrics.items():
        if any(key.startswith(prefix) for prefix in exclude_prefixes):
            continue

        if isinstance(value, dict):
            wandb_metrics[key] = prepare_metrics_for_wandb(value, exclude_prefixes)
        else:
            if is_immutable(value):
                wandb_metrics[key] = value
            else:
                value_array = np.asarray(value)
                if value_array.ndim == 1:
                    wandb_metrics[key] = value_array.mean().item()
                    wandb_metrics[f"{key}_std"] = value_array.std().item()

    return wandb_metrics


Punct = r"[«»\"'“”‘’.,;:!?…—\-(){}\[\]]"

def normalize_string(s: str) -> str:
    s = (s or "").lower().strip()
    s = s.replace("ё", "е")

    # allow conjunction normalization (comma vs "и")
    s = re.sub(r"\bи\b", " ", s)

    s = re.sub(Punct, " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def extract_tag_content(text, tag=None):
    return re.findall(rf"<{tag}>(.*?)</{tag}>", text, flags=re.S | re.I)