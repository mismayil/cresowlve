import argparse
import pathlib
import re
import random

from cresowlve.utils import write_json, find_files, read_json, extract_tag_content

def parse_question(question):
    prefix_pattern = r'^\s*\[([^\]]+)\]'
    match = re.match(prefix_pattern, question, flags=re.DOTALL)
    if match:
        question = question[match.end():].strip()
        prefix = match.group(1)
        return question, prefix
    return question, None

def prepare_chgk_data(datapath):
    data = read_json(datapath)
    task_data = []
    for sample in data["data"]:
        task_sample = {**sample, "question_prefix": None}
        question, prefix = parse_question(sample["question"])
        task_sample["question"] = question
        task_sample["question_prefix"] = prefix
        task_data.append(task_sample)
    return task_data

def prepare_chgk_no_external_mat_data(datapath):
    data = read_json(datapath)
    task_data = []

    for sample in data["data"]:
        if sample["output"].lower() == "no":
            task_data.append({
                "id": sample["id"]
            })

    return task_data

def prepare_chgk_translated_data(datapath):
    data = read_json(datapath)
    task_data = []

    for sample in data["data"]:
        task_sample = {
            "id": sample["id"]
        }
        question = extract_tag_content(sample["output"], tag="Question")
        answer = extract_tag_content(sample["output"], tag="Answer")
        comment = extract_tag_content(sample["output"], tag="Comment")
        notes = extract_tag_content(sample["output"], tag="Notes")
        
        if question:
            question, prefix = parse_question(question[0].strip())
            task_sample["question_en"] = question
            task_sample["question_prefix_en"] = prefix
        else:
            print(f"Warning: No question found for sample ID {sample['id']}")
        if answer:
            task_sample["answer_en"] = answer[0].strip()
        else:
            print(f"Warning: No answer found for sample ID {sample['id']}")
        if comment:
            task_sample["comment_en"] = comment[0].strip()
        else:
            print(f"Warning: No comment found for sample ID {sample['id']}")
        if notes:
            task_sample["notes_en"] = notes[0].strip()
        else:
            print(f"Warning: No notes found for sample ID {sample['id']}")
        task_data.append(task_sample)

    return task_data

def prepare_chgk_ru_specific_annot_data(datapath):
    data = read_json(datapath)
    task_data = []

    for sample in data["data"]:
        task_sample = {
            "id": sample["id"]
        }
        reasoning = extract_tag_content(sample["output"], tag="Reasoning")
        answer = extract_tag_content(sample["output"], tag="Answer")

        if reasoning:
            task_sample["ru_spec_reasoning_en"] = reasoning[0].strip()
        else:
            print(f"Warning: No reasoning found for sample ID {sample['id']}")
        if answer:
            task_sample["ru_spec_answer_en"] = answer[0].strip()
        else:
            print(f"Warning: No answer found for sample ID {sample['id']}")

        task_data.append(task_sample)

    return task_data

def prepare_chgk_no_ru_spec_filtered_data(datapath):
    data = read_json(datapath)
    task_data = []

    for sample in data["data"]:
        if sample["ru_spec_answer_en"].lower() == "no":
            task_data.append({
                "id": sample["id"]
            })

    return task_data

def prepare_chgk_benchmark_data(datapaths):
    task_data = []
    question_set = set()

    for datapath in datapaths:
        data = read_json(datapath)

        for sample in data["data"]:
            if sample["question"] not in question_set:
                if sample["annot_check"] in ["1", "2", "4", "6"]:
                    question_set.add(sample["question"])
                    task_data.append(sample)
            else:
                print(f"Duplicate question found: (ID: {sample['id']})")
    
    return task_data

def prepare_chgk_en_benchmark_data(datapath):
    task_data = []
    data = read_json(datapath)

    for sample in data["data"]:
        en_sample = {}
        for key, value in sample.items():
            if key.endswith("_en") or f"{key}_en" not in sample:
                en_sample[key.replace("_en", "")] = value
        task_data.append(en_sample)
    
    return task_data

def prepare_chgk_ru_benchmark_data(datapath):
    task_data = []
    data = read_json(datapath)

    for sample in data["data"]:
        en_sample = {}
        for key, value in sample.items():
            if not key.endswith("_en"):
                en_sample[key] = value
        task_data.append(en_sample)
    
    return task_data

def prepare_chgk_benchmark_reasoning_types_data(datapath):
    task_data = []
    data = read_json(datapath)

    for sample in data["data"]:
        task_sample = {
            "id": sample["id"]
        }
        reasoning_type = extract_tag_content(sample["output"], tag="Answer")
        concepts = extract_tag_content(sample["output"], tag="concept")
        if reasoning_type:
            task_sample["reasoning_type"] = reasoning_type[0].strip()
        if concepts:
            task_sample["concepts"] = [c.strip() for c in concepts]
        task_data.append(task_sample)
    
    return task_data

def prepare_chgk_benchmark_knowledge_data(datapath):
    task_data = []
    data = read_json(datapath)

    for sample in data["data"]:
        task_sample = {
            "id": sample["id"]
        }
        knowledge = extract_tag_content(sample["output"], tag="knowledge")
        if knowledge:
            task_sample["knowledge"] = [k.strip() for k in knowledge]
        task_data.append(task_sample)
    
    return task_data


def prepare_chgk_benchmark_domain_data(datapath):
    task_data = []
    data = read_json(datapath)

    for sample in data["data"]:
        task_sample = {
            "id": sample["id"]
        }
        domains = extract_tag_content(sample["output"], tag="domain")
        if domains:
            task_sample["domains"] = [d.strip() for d in domains]
        task_data.append(task_sample)
    
    return task_data

def prepare_chgk_benchmark_knowledge_source_data(datapath):
    task_data = []
    data = read_json(datapath)

    for sample in data["data"]:
        task_sample = {
            "id": sample["id"]
        }
        task_sample["knowledge_source"] = sample["output"].strip().strip('"').strip("'")
        task_data.append(task_sample)
    
    return task_data

def prepare_chgk_benchmark_grouped_domain_data(datapaths):
    task_data = []
    assert len(datapaths) == 2, "Expected exactly 2 files for grouped domain data preparation"
    data = read_json(datapaths[0])
    domain_mapping = read_json(datapaths[1])

    for sample in data["data"]:
        domains = sample["domains"]
        grouped_domains = set()
        for domain in domains:
            group_domain_found = False
            for group_domain, group_members in domain_mapping["data"].items():
                if domain.lower() in [m.lower() for m in group_members] or domain.lower() == group_domain.lower():
                    grouped_domains.add(group_domain)
                    group_domain_found = True
                    break
            if not group_domain_found:
                print(f"Warning: No group domain found for domain '{domain}' in sample ID {sample['id']}")
        sample["grouped_domains"] = list(grouped_domains)
        task_data.append(sample)
    
    return task_data

def prepare_chgk_benchmark_culture_lang_data(datapath):
    task_data = []
    data = read_json(datapath)

    for sample in data["data"]:
        task_sample = {
            "id": sample["id"]
        }
        task_sample["culture_langs"] = [c.strip() for c in sample["output"].strip().split(",")]
        task_data.append(task_sample)
    
    return task_data

def prepare_chgk_benchmark_error_annot_data(datapath):
    task_data = []
    data = read_json(datapath)

    for sample in data["data"]:
        output = sample["output"].strip()
        error_reasonings = extract_tag_content(output, tag="Reasoning")
        error_categories = extract_tag_content(output, tag="Category")
        task_sample = {
            "id": sample["id"],
            "error_reasoning": error_reasonings[-1].strip(),
            "error_category": error_categories[-1].strip()
        }
        task_data.append(task_sample)
    
    return task_data

def prepare_chgk_benchmark_results_error_data(datapath):
    task_data = []
    data = read_json(datapath)

    for sample in data["data"]:
        if not sample.get("gpt-4o_judge_match", False):
            task_sample = {
                "id": sample["id"]
            }
            task_data.append(task_sample)
    
    return task_data

def prepare_chgk_benchmark_contamination_data(datapaths):
    model_outputs = read_json(datapaths[0])
    benchmark_data = read_json(datapaths[1])
    task_data = []

    for sample in model_outputs["data"]:
        if sample.get("exact_match", False):
            benchmark_sample = next((s for s in benchmark_data["data"] if s["id"] == sample["id"]), None)
            question = benchmark_sample["question"]
            words = question.split()
            random_cutoff  = random.choice(list(range(2, len(words)-2)))
            question_prefix = " ".join(words[:random_cutoff])
            question_suffix = " ".join(words[random_cutoff:])
            task_sample = {
                "id": sample["id"],
                "q_prefix": question_prefix,
                "q_suffix": question_suffix,
            }
            task_data.append(task_sample)
    
    return task_data

def prepare_chgk_benchmark_contamination_data_by_en_ru_diff(datapaths):
    model_outputs1 = read_json(datapaths[0])     # must be the English benchmark outputs
    model_outputs2 = read_json(datapaths[1])     # must be the Russian benchmark outputs
    benchmark_data = read_json(datapaths[2])
    task_data = []

    en0_ids = set(sample["id"] for sample in model_outputs1["data"] if not sample.get("exact_match", False))
    ru1_ids = set(sample["id"] for sample in model_outputs2["data"] if sample.get("exact_match", False))
    en0_ru1_ids = en0_ids.intersection(ru1_ids)

    for sample in model_outputs1["data"]:
        if sample["id"] in en0_ru1_ids:
            benchmark_sample = next((s for s in benchmark_data["data"] if s["id"] == sample["id"]), None)
            question = benchmark_sample["question"]
            words = question.split()
            random_cutoff  = random.choice(list(range(2, len(words)-2)))
            question_prefix = " ".join(words[:random_cutoff])
            question_suffix = " ".join(words[random_cutoff:])
            task_sample = {
                "id": sample["id"],
                "q_prefix": question_prefix,
                "q_suffix": question_suffix,
            }
            task_data.append(task_sample)
    
    return task_data

def prepare_chgk_benchmark_contamination_control_data_by_en_ru_diff(datapaths):
    model_outputs1 = read_json(datapaths[0])     # must be the English benchmark outputs
    model_outputs2 = read_json(datapaths[1])     # must be the Russian benchmark outputs
    benchmark_data = read_json(datapaths[2])
    task_data = []

    en0_ids = set(sample["id"] for sample in model_outputs1["data"] if not sample.get("exact_match", False))
    ru0_ids = set(sample["id"] for sample in model_outputs2["data"] if not sample.get("exact_match", False))
    en0_ru0_ids = en0_ids.intersection(ru0_ids)

    for sample in model_outputs1["data"]:
        if sample["id"] in en0_ru0_ids:
            benchmark_sample = next((s for s in benchmark_data["data"] if s["id"] == sample["id"]), None)
            question = benchmark_sample["question"]
            words = question.split()
            random_cutoff  = random.choice(list(range(2, len(words)-2)))
            question_prefix = " ".join(words[:random_cutoff])
            question_suffix = " ".join(words[random_cutoff:])
            task_sample = {
                "id": sample["id"],
                "q_prefix": question_prefix,
                "q_suffix": question_suffix,
            }
            task_data.append(task_sample)
    
    return task_data

def prepare_chgk_benchmark_data_contamination_quiz_annot_data(datapaths):
    model_outputs = read_json(datapaths[0])
    benchmark_data = read_json(datapaths[1])
    task_data = []

    for sample in model_outputs["data"]:
        benchmark_sample = next((s for s in benchmark_data["data"] if s["id"] == sample["id"]), None)
        options = extract_tag_content(sample["output"], tag="option")
        if not options:
            options = extract_tag_content(sample["output"], tag="options")
        correct_option = benchmark_sample["question"].strip().replace("\n", " ")
        options = [o.strip().replace("\n", " ") for o in options if o.strip()]
        options = options + [correct_option]
        options = list(set(options))
        if len(options) == 4:
            shuffled_options = random.sample(options, len(options))
            correct_option_index = shuffled_options.index(correct_option)
            task_sample = {
                "id": sample["id"],
                "option_a": shuffled_options[0],
                "option_b": shuffled_options[1],
                "option_c": shuffled_options[2],
                "option_d": shuffled_options[3],
                "correct_option": "abcd"[correct_option_index]
            }
            task_data.append(task_sample)
        else:
            print(f"Warning: Expected 4 unique options (including the correct question) for sample ID {sample['id']}, but got {len(options)}. Skipping this sample.")
    
    return task_data

def prepare_chgk_benchmark_data_contamination_quiz_bdq(datapath):
    model_outputs = read_json(datapath)
    task_data = []

    for sample in model_outputs["data"]:
        correct_option = sample["correct_option"]
        other_options = [sample[f"option_{o}"] for o in "abcd" if f"option_{o}" in sample and o != correct_option]
        task_data.append({
            "id": sample["id"],
            "option_a": other_options[0],
            "option_b": other_options[1],
            "option_c": other_options[2],
            "correct_option": sample[f"option_{correct_option}"]
        })
    
    return task_data

def prepare_chgk_benchmark_data_contamination_quiz_bcq(datapaths):
    model_outputs = read_json(datapaths[0])
    bdq_data = read_json(datapaths[1])
    non_preferred_positions = [pos for pos, freq in model_outputs["metrics"]["pos_freqs"].items() if freq < (len(model_outputs["data"]) / 4) and pos in ["a", "b", "c"]]

    task_data = []

    for sample in bdq_data["data"]:
        correct_pos = random.choice(non_preferred_positions)
        other_positions = [p for p in ["a", "b", "c"] if p != correct_pos]
        task_data.append({
            "id": sample["id"],
            f"option_{correct_pos}": sample["correct_option"],
            f"option_{other_positions[0]}": sample[f"option_{other_positions[0]}"],
            f"option_{other_positions[1]}": sample[f"option_{other_positions[1]}"],
            "correct_option": correct_pos
        })

    return task_data

TASK_MAP = {
    "chgk": prepare_chgk_data,
    "chgk_no_external_mat": prepare_chgk_no_external_mat_data,
    "chgk_translated": prepare_chgk_translated_data,
    "chgk_ru_specific_annot": prepare_chgk_ru_specific_annot_data,
    "chgk_ru_spec_filtered": prepare_chgk_no_ru_spec_filtered_data,
    "chgk_benchmark": prepare_chgk_benchmark_data,
    "chgk_en_benchmark": prepare_chgk_en_benchmark_data,
    "chgk_ru_benchmark": prepare_chgk_ru_benchmark_data,
    "chgk_benchmark_reasoning_types": prepare_chgk_benchmark_reasoning_types_data,
    "chgk_benchmark_knowledge": prepare_chgk_benchmark_knowledge_data,
    "chgk_benchmark_knowledge_source": prepare_chgk_benchmark_knowledge_source_data,
    "chgk_benchmark_domain": prepare_chgk_benchmark_domain_data,
    "chgk_benchmark_grouped_domain": prepare_chgk_benchmark_grouped_domain_data,
    "chgk_benchmark_culture_lang": prepare_chgk_benchmark_culture_lang_data,
    "chgk_benchmark_error_annot": prepare_chgk_benchmark_error_annot_data,
    "chgk_benchmark_results_error": prepare_chgk_benchmark_results_error_data,
    "chgk_benchmark_contamination": prepare_chgk_benchmark_contamination_data,
    "chgk_benchmark_contamination_by_en_ru_diff": prepare_chgk_benchmark_contamination_data_by_en_ru_diff,
    "chgk_benchmark_contamination_quiz_annot": prepare_chgk_benchmark_data_contamination_quiz_annot_data,
    "chgk_benchmark_contamination_quiz_bdq": prepare_chgk_benchmark_data_contamination_quiz_bdq,
    "chgk_benchmark_contamination_quiz_bcq": prepare_chgk_benchmark_data_contamination_quiz_bcq,
    "chgk_benchmark_contamination_control_by_en_ru_diff": prepare_chgk_benchmark_contamination_control_data_by_en_ru_diff,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-paths", type=str, nargs="+", help="Path to input data file(s) in json", required=True)
    parser.add_argument("-t", "--task", type=str, default="chgk", help="Task name")
    parser.add_argument("-s", "--suffix", type=str, default="", help="Custom suffix for output file path.")
    parser.add_argument("-o", "--output-path", type=str, help="Output file path", required=True)
    parser.add_argument("--process-together", action="store_true", help="Whether to process all files together or separately")

    args = parser.parse_args()
    files_to_process = []

    for input_path in args.input_paths:
        if pathlib.Path(input_path).is_file():
            files_to_process.append(input_path)
        else:
            files_to_process.extend(find_files(input_path))

    if args.process_together:
        task_data = TASK_MAP[args.task](files_to_process)
    else:
        task_data = []

        for file_path in files_to_process:
            task_data.extend(TASK_MAP[args.task](file_path))

    output_path = pathlib.Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_data = {
        "metadata": {
            "source": args.input_paths,
            "task": args.task,
            "size": len(task_data)
        },
        "data": task_data
    }

    write_json(output_data, output_path.with_suffix(".json"))

if __name__ == "__main__":
    main()