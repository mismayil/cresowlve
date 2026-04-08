import argparse
import pathlib
from tqdm import tqdm
import random

from cresowlve.utils import read_json, write_json, get_template_keys
from cresowlve.prompts import *

USER_INSTRUCTION_TEMPLATES = {
    "ext_mat_annot": EXTERNAL_MATERIAL_ANNOTATION,
    "translate_puzzle_ru_to_en": TRANSLATE_PUZZLE_RU_TO_EN,
    "ru_spec_annot": RUSSIAN_SPECIFIC_ANNOTATION_INSTR,
    "cot_only_final_answer_ru_en": COT_ONLY_FINAL_ANSWER_RU_EN,
    "cot_only_final_answer_en": COT_ONLY_FINAL_ANSWER_EN,
    "cot_answer_ru_en": COT_ANSWER_RU_EN,
    "cot_answer_en": COT_ANSWER_EN,
    "reasoning_model_en": REASONING_MODEL_EN,
    "reasoning_model_ru_en": REASONING_MODEL_RU_EN,
    "reasoning_type_annot": REASONING_TYPE_ANNOTATION,
    "knowledge_annot": KNOWLEDGE_ANNOTATION,
    "domain_annot": DOMAIN_ANNOTATION,
    "knowledge_source_annot": KNOWLEDGE_SOURCE_ANNOTATION,
    "culture_lang_annot": CULTURE_LANG_ANNOTATION,
    "error_annot": ERROR_ANNOTATION,
    "data_contamination_guided_en": DATA_CONTAMINATION_GUIDED_EN,
    "data_contamination_general_en": DATA_CONTAMINATION_GENERAL_EN,
    "data_contamination_quiz_annot": DATA_CONTAMINATION_QUIZ_ANNOTATION,
    "data_contamination_quiz_mcq": DATA_CONTAMINATION_QUIZ_MCQ,
    "data_contamination_quiz_bdq": DATA_CONTAMINATION_QUIZ_BDQ,
    "data_contamination_quiz_bcq": DATA_CONTAMINATION_QUIZ_BCQ
}

SHOT_TEMPLATES = {
    "ru_spec_annot": RUSSIAN_SPECIFIC_ANNOTATION_SHOT,
    "domain_annot": DOMAIN_ANNOTATION_SHOT,
    "knowledge_annot": KNOWLEDGE_ANNOTATION_SHOT,
    "reasoning_type_annot": REASONING_TYPE_ANNOTATION_SHOT,
    "knowledge_source_annot": KNOWLEDGE_SOURCE_ANNOTATION_SHOT,
    "culture_lang_annot": CULTURE_LANG_ANNOTATION_SHOT,
    "error_annot": ERROR_ANNOTATION_SHOT
}

def prepare_prompt_value(value, list_delimiter="\n"):
    if isinstance(value, list):
        return list_delimiter.join(value)
    return value

def prepare_prompt(sample, template, list_delimiter="\n"):
    template_keys = get_template_keys(template)
    format_args = {k: prepare_prompt_value(sample.get(k, "N/A"), list_delimiter=list_delimiter) for k in template_keys}
    return template.format(**format_args)

def prepare_user_instruction(sample, template, list_delimiter="\n"):
    instruction_template = USER_INSTRUCTION_TEMPLATES[template]
    return prepare_prompt(sample, instruction_template, list_delimiter=list_delimiter).strip()

def prepare_shot(sample, template, num_shots=1, shot_data=None, answer_fields=None, list_delimiter="\n", shuffle_shots=False):
    if not shot_data:
        return ""

    if not answer_fields:
        answer_fields = []
    
    shot_samples = shot_data["data"][:num_shots]

    if shuffle_shots:
        random.shuffle(shot_samples)

    shot_template = SHOT_TEMPLATES[template]
    shots = []

    for i, shot_sample in enumerate(shot_samples):
        shots.append(
            prepare_prompt({**shot_sample, "index": i+1}, shot_template, list_delimiter=list_delimiter).strip()
        )

    final_shot = prepare_prompt({**sample, "index": len(shot_samples)+1, **{f: "" for f in answer_fields}}, shot_template, list_delimiter=list_delimiter).strip()
    return "\n\n".join(shots + [final_shot]).strip()

USER_INSTRUCTION_PROCESSORS = {
    "default": prepare_user_instruction
}

SHOT_PROCESSORS = {
    "default": prepare_shot
}

def prepare_sample_for_eval(sample, template, num_shots=1, shot_data=None, answer_fields=None, list_delimiter="\n", shuffle_shots=False):
    user_instr_processor = USER_INSTRUCTION_PROCESSORS.get(
        template, USER_INSTRUCTION_PROCESSORS["default"]
    )
    shot_processor = SHOT_PROCESSORS.get(
        template, SHOT_PROCESSORS["default"]
    )
    
    eval_data = []
        
    user_prompt = user_instr_processor(sample, template, list_delimiter=list_delimiter)
    shot_prompt = shot_processor(sample, template, num_shots=num_shots, shot_data=shot_data, answer_fields=answer_fields, list_delimiter=list_delimiter, shuffle_shots=shuffle_shots)

    if shot_prompt:
        user_prompt += "\n\n" + shot_prompt

    eval_data.append(
        {
            "id": sample["id"],
            "user_prompt": user_prompt.strip()
        }
    )

    return eval_data

def extend_by_source_data(data, source_data_lst):
    for source_data in source_data_lst or []:
        source_data_dict = {item["id"]: item for item in source_data["data"]}
        for sample in data["data"]:
            if sample["id"] in source_data_dict:
                sample.update(source_data_dict[sample["id"]])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datapath", type=str, help="Path to task data in json", required=True)
    parser.add_argument("--source-datapaths", nargs="*", type=str, help="Paths to source task data in json")
    parser.add_argument("-t", "--template", type=str, default="default_zs_cot", help="Template name")
    parser.add_argument(
        "-s",
        "--suffix",
        type=str,
        default="",
        help="Custom suffix for output file path.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default=None,
        help="Output directory path. Defaults to input directory path.",
    )
    parser.add_argument("-sp", "--shot-path", type=str, default=None, help="Path to shot examples in json")
    parser.add_argument("-n", "--num-shots", type=int, default=-1, help="Number of shot examples to include")
    parser.add_argument("--answer-fields", nargs="*", default=["shot_answer"], help="Fields to include in the answer output")
    parser.add_argument("--list-delimiter", type=str, default="\n", help="Delimiter to use when joining list values in the prompt")
    parser.add_argument("--shuffle-shots", action="store_true", help="Shuffle order of shots for each sample")

    args = parser.parse_args()
    input_data = read_json(args.datapath)
    shot_data = read_json(args.shot_path) if args.shot_path is not None else None
    source_data_lst = [read_json(p) for p in args.source_datapaths] if args.source_datapaths else None

    if shot_data:
        if args.num_shots < 0:
            args.num_shots = len(shot_data["data"])
    else:
        args.num_shots = 0

    extend_by_source_data(input_data, source_data_lst)
    
    if shot_data:
        extend_by_source_data(shot_data, source_data_lst)

    eval_data = []

    for sample in tqdm(input_data["data"], desc="Preparing task data for evaluation"):
            eval_data.extend(
                prepare_sample_for_eval(
                    sample,
                    template=args.template,
                    num_shots=args.num_shots,
                    shot_data=shot_data,
                    answer_fields=args.answer_fields,
                    list_delimiter=args.list_delimiter,
                    shuffle_shots=args.shuffle_shots
                )
            )

    datapath = pathlib.Path(args.datapath)
    output_dir = pathlib.Path(args.output_dir) if args.output_dir is not None else datapath.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    eval_data_path = output_dir / f"{datapath.stem}_eval_{args.template}_s{args.num_shots}{args.suffix}.json"

    output_data = {
        "metadata": {
            "source": args.datapath,
            "template": args.template,
            "size": len(eval_data),
            "shot_path": args.shot_path,
            "source_datapaths": args.source_datapaths,
            "answer_fields": args.answer_fields,
            "list_delimiter": args.list_delimiter,
            "shuffle_shots": args.shuffle_shots
        },
        "data": eval_data
    }
    write_json(output_data, eval_data_path)

    print(f"Output data saved to {eval_data_path}")


if __name__ == "__main__":
    main()