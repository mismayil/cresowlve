import argparse
from tqdm import tqdm
import pathlib
from statistics import mean
import re
import asyncio
from dotenv import load_dotenv

from cresowlve.prompts import LLM_JUDGE_WITH_CONTEXT_EN
from cresowlve.utils import read_json, write_json, find_files, compute_usage, prepare_metrics_for_wandb, wandb_log_run, normalize_string, extract_tag_content
from cresowlve.inference_lm import get_inference_service
from cresowlve.prepare_eval_data import prepare_prompt

LLM_JUDGE_TEMPLATES = {
    "en_with_context": LLM_JUDGE_WITH_CONTEXT_EN
}

def extract_prediction(sample, output_attr="output"):
    text = (sample.get(output_attr) or "").strip()
    answers = extract_tag_content(text, tag="Answer")
    if answers:
        return answers[-1].strip()
    m2 = re.findall(r"<Answer>\s*(.*)\Z", text, flags=re.S | re.I)
    if m2:
        return m2[-1].strip()
    return text

def extract_reasoning(sample, output_attr="output"):
    text = (sample.get(output_attr) or "").strip()
    reasonings = extract_tag_content(text, tag="Reasoning")
    if reasonings:
        return "\n".join(reasonings)
    # if answer is in the output with Answer tags, take everything else as reasoning
    if re.search(r"<Answer>.*?</Answer>", text, flags=re.S | re.I):
        reasoning = re.sub(r"<Answer>.*?</Answer>", "", text, flags=re.S | re.I).strip()
        return reasoning
    return None

async def get_llm_judge_prediction(sample, llm_judge_template="en_with_context", llm_judge_model="gpt-4o"):
    user_prompt = prepare_prompt(sample, LLM_JUDGE_TEMPLATES[llm_judge_template])
    service = get_inference_service(llm_judge_model)
    responses = await service.generate([{"id": sample["id"], "user_prompt": user_prompt}])
    response = responses[0]
    text = response.text.strip().lower()
    return text if text else response.exception

async def compute_metrics(results, report_usage=True, llm_judge_template="en_with_context", llm_judge_model="gpt-4o", source_datapath=None, 
                          force_rejudge=False, output_field=None, reference_field=None):
    metrics = {}

    usage = {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0
    }

    cost = {
        "input": 0,
        "output": 0,
        "total": 0
    }

    source_data_dict = {}

    if source_datapath:
        source_data = read_json(source_datapath)
        source_data_dict = {item["id"]: item for item in source_data["data"]}

    for result_idx, result in tqdm(enumerate(results["data"]), total=len(results["data"]), desc="Computing metrics"):
        if output_field in result:
            result_source = source_data_dict.get(result["id"], {})
            result["reference"] = result_source[reference_field]
            result["prediction"] = extract_prediction(result, output_attr=output_field)
            result["reasoning"] = extract_reasoning(result, output_attr=output_field)
            result["exact_match"] = normalize_string(result["reference"]) == normalize_string(result["prediction"])

            llm_judge_attr = f"{llm_judge_model}_judge_pred"
            if llm_judge_attr not in result or force_rejudge:
                result[llm_judge_attr] = await get_llm_judge_prediction({**result, **result_source}, llm_judge_template=llm_judge_template, llm_judge_model=llm_judge_model)
            result[f"{llm_judge_model}_judge_match"] = normalize_string(result[llm_judge_attr]) == "yes"

            if report_usage:
                sample_usage, sample_cost = compute_usage(result, results["metadata"]["model"])
                if sample_usage:
                    usage["input_tokens"] += sample_usage["input_tokens"]
                    usage["output_tokens"] += sample_usage["output_tokens"]
                    usage["total_tokens"] += sample_usage["input_tokens"] + sample_usage["output_tokens"]
                if sample_cost:
                    cost["input"] += sample_cost["input"]
                    cost["output"] += sample_cost["output"]
                    cost["total"] += sample_cost["total"]

    metrics["num_samples"] = len(results["data"])
    metrics["exact_match_acc"] = mean([int(r.get("exact_match", False)) for r in results["data"]])
    metrics[f"{llm_judge_model}_judge_acc"] = mean([int(r.get(f"{llm_judge_model}_judge_match", False)) for r in results["data"]])

    if report_usage:
        metrics["usage"] = usage
        metrics["cost"] = cost

    return metrics


async def report_metrics(results_files, report_usage=True, llm_judge_template="en_with_context", llm_judge_model="gpt-4o", source_datapath=None, 
                         force_rejudge=False, output_field=None, reference_field=None):
    for results_file in tqdm(results_files, total=len(results_files), desc="Reporting metrics"):
        results = read_json(results_file)
        if "data" in results:
            metrics = await compute_metrics(results, report_usage=report_usage, llm_judge_template=llm_judge_template, 
                                            llm_judge_model=llm_judge_model, source_datapath=source_datapath, force_rejudge=force_rejudge,
                                            output_field=output_field,
                                            reference_field=reference_field)
            results["metrics"] = metrics
            results["metadata"]["llm_judge_template"] = llm_judge_template
            results["metadata"]["llm_judge_model"] = llm_judge_model
            results["metadata"]["output_field"] = output_field
            results["metadata"]["reference_field"] = reference_field
            write_json(results, results_file)
            wandb_metrics = prepare_metrics_for_wandb(metrics)
            wandb_log_run(name=results["metadata"]["model"], config=results["metadata"], metrics=wandb_metrics)


async def main():
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--results-path", type=str, help="Path to evaluation results (file or dir)", required=True)
    parser.add_argument("-u", "--report-usage", action="store_true", help="Report usage metrics", default=True)
    parser.add_argument("--llm-judge-model", type=str, default="gpt-4o", help="LLM model to use for judging model responses")
    parser.add_argument("--llm-judge-template", type=str, choices=LLM_JUDGE_TEMPLATES.keys(), default="en_with_context", help="Template to use for LLM judge")
    parser.add_argument("--source-datapath", type=str, help="Path to source task data in json")
    parser.add_argument("--force-rejudge", action="store_true", help="Force re-judging even if judge prediction already exists in results")
    parser.add_argument("--output-field", type=str, default="output", help="Field in results containing model output to evaluate")
    parser.add_argument("--reference-field", type=str, default="answer", help="Field in source data containing reference answer")

    args = parser.parse_args()

    files_to_process = []
    results_path = pathlib.Path(args.results_path)
    if results_path.is_file():
        files_to_process.append(args.results_path)
    else:
        files_to_process.extend(find_files(args.results_path))

    await report_metrics(files_to_process, args.report_usage, llm_judge_template=args.llm_judge_template, 
                         llm_judge_model=args.llm_judge_model, source_datapath=args.source_datapath, force_rejudge=args.force_rejudge,
                         output_field=args.output_field, reference_field=args.reference_field)


if __name__ == "__main__":
    asyncio.run(main())
