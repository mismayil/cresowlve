import spacy
from collections import Counter
from statistics import mean
from dotenv import load_dotenv
import argparse
import pathlib
from tqdm import tqdm
from itertools import combinations
import evaluate

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim, dot_score, euclidean_sim, manhattan_sim

from cresowlve.utils import cache, find_files, read_json, write_json, compute_usage

DEF_EMB_MODEL = "thenlper/gte-large"
DEF_EMB_TYPE = "sentence_embedding"
DEF_EMB_STRATEGY = "direct"
DEF_DIST_FN = "cosine"
DEF_SPACY_LANG = "en_core_web_sm"
DEF_PREPROCESSING_ARGS = {
    "lower": True,
    "remove_punct": True,
    "remove_stopwords": True,
    "lemmatize": True,
    "dominant_k": None,
    "unique": True
}

SPACY_ENGINE_CACHE = {}
EMB_MODEL_CACHE = {}
EMBEDDING_CACHE = {}
SPACY_CACHE = {}

@cache(cache_dict=SPACY_ENGINE_CACHE)
def load_spacy_engine(language=DEF_SPACY_LANG):
    print(f"Loading spacy engine: {language}")
    engine = spacy.load(language)
    return engine

@cache(cache_dict=EMB_MODEL_CACHE)
def load_emb_model(model=DEF_EMB_MODEL):
    print(f"Loading embedding model: {model}")
    return SentenceTransformer(model)

@cache(cache_dict=EMBEDDING_CACHE)
def get_embedding(text, model=DEF_EMB_MODEL, emb_type=DEF_EMB_TYPE):
    emb_model = load_emb_model(model)
    
    output_value = "sentence_embedding"

    if "token" in emb_type:
        output_value = "token_embeddings"

    embeddings = emb_model.encode(text, output_value=output_value)
    
    if embeddings.ndim == 2:
        embeddings = embeddings.mean(axis=0)

    return embeddings

@cache(cache_dict=SPACY_CACHE)
def get_spacy_doc(text):
    spacy_engine = load_spacy_engine()
    return spacy_engine(text)

def compute_sem_dis(emb1, emb2, distance_fn=DEF_DIST_FN):
    if distance_fn == "cosine":
        return (1 - cos_sim(emb1, emb2)).item()
    elif distance_fn == "dot":
        return (1 - dot_score(emb1, emb2)).item()
    elif distance_fn == "euclidean":
        return (-euclidean_sim(emb1, emb2)).item()
    elif distance_fn == "manhattan":
        return (-manhattan_sim(emb1, emb2)).item()
    else:
        raise ValueError(f"Invalid distance function: {distance_fn}")

def get_sentences(text):
    doc = get_spacy_doc(text)
    return [sent.text for sent in doc.sents]

def get_words(text, lower=True, remove_punct=True, remove_stopwords=True, lemmatize=True, unique=True, dominant_k=None):
    doc = get_spacy_doc(text)
    tokens = [token for token in doc]

    if remove_punct:
        tokens = [token for token in tokens if not token.is_punct]
    
    if remove_stopwords:
        tokens = [token for token in tokens if not token.is_stop]

    words = [token.text for token in tokens]

    if lemmatize:
        words = [token.lemma_ for token in tokens]
    
    if lower:
        words = [word.lower() for word in words]
    
    if dominant_k is None or dominant_k == 0 or dominant_k >= len(words):
        if unique:
            return list(set(words))
        return words

    word_freq = Counter(words)

    return [w[0] for w in word_freq.most_common(dominant_k)]

def compute_text_embedding(text, emb_model=DEF_EMB_MODEL, emb_type=DEF_EMB_TYPE, emb_strategy=DEF_EMB_STRATEGY,
                            preprocessing_args=DEF_PREPROCESSING_ARGS):
    if emb_strategy == "direct":
        return get_embedding(text, emb_model, emb_type)
    elif emb_strategy == "by_word":
        words = get_words(text, **preprocessing_args)
        return get_embedding(words, emb_model, emb_type)
    elif emb_strategy == "by_sentence":
        sentences = get_sentences(text)
        return get_embedding(sentences, emb_model, emb_type)
    else:
        raise ValueError(f"Invalid embedding strategy: {emb_strategy}")

def compute_avg_pairwise_distances(embeddings, distance_fn=DEF_DIST_FN):
    if len(embeddings) <= 1:
        return [0]

    avg_pairwise_distances = []
    for i in range(len(embeddings)):
        pairwise_distances = []
        for j in range(len(embeddings)):
            if i != j:
                distance = compute_sem_dis(embeddings[i], embeddings[j], distance_fn)
                pairwise_distances.append(distance)
        avg_pairwise_distances.append(mean(pairwise_distances))
    return avg_pairwise_distances

def compute_dsi(text, emb_model=DEF_EMB_MODEL, emb_type=DEF_EMB_TYPE, distance_fn=DEF_DIST_FN, preprocessing_args=DEF_PREPROCESSING_ARGS):
    words = get_words(text, **preprocessing_args)
    embeddings = [get_embedding(word, emb_model, emb_type) for word in words]
    return mean(compute_avg_pairwise_distances(embeddings, distance_fn))

def compute_domain_semdis(input_data, **kwargs):
    data = input_data["data"]
    for sample in tqdm(data, desc="Computing domain semantic distance"):
        domains = sample.get("domains", [])
        if len(domains) > 1:
            domain_embs = [compute_text_embedding(domain) for domain in domains]
            sample["domain_semdis"] = mean(compute_avg_pairwise_distances(domain_embs))
        else:
            sample["domain_semdis"] = 0
    return {"domain_semdis": mean([sample["domain_semdis"] for sample in data])}

def compute_max_domain_semdis(input_data, **kwargs):
    data = input_data["data"]
    for sample in tqdm(data, desc="Computing max domain semantic distance"):
        domains = sample.get("domains", [])
        if len(domains) > 1:
            domain_embs = [compute_text_embedding(domain) for domain in domains]
            max_domain_semdis = None
            for emb1, emb2 in combinations(domain_embs, 2):
                semdis = compute_sem_dis(emb1, emb2)
                if max_domain_semdis is None or semdis > max_domain_semdis:
                    max_domain_semdis = semdis
            sample["max_domain_semdis"] = max_domain_semdis
        else:
            sample["max_domain_semdis"] = 0
    return {"max_domain_semdis": mean([sample["max_domain_semdis"] for sample in data])}

def compute_knowledge_semdis(input_data, **kwargs):
    data = input_data["data"]
    for sample in tqdm(data, desc="Computing knowledge semantic distance"):
        knowledge = sample.get("knowledge", [])
        if len(knowledge) > 1:
            knowledge_embs = [compute_text_embedding(knowledge) for knowledge in knowledge]
            sample["knowledge_semdis"] = mean(compute_avg_pairwise_distances(knowledge_embs))
        else:
            sample["knowledge_semdis"] = 0
    return {"knowledge_semdis": mean([sample["knowledge_semdis"] for sample in data])}

def compute_max_knowledge_semdis(input_data, **kwargs):
    data = input_data["data"]
    for sample in tqdm(data, desc="Computing max knowledge semantic distance"):
        knowledge = sample.get("knowledge", [])
        if len(knowledge) > 1:
            knowledge_embs = [compute_text_embedding(knowledge) for knowledge in knowledge]
            max_knowledge_semdis = None
            for emb1, emb2 in combinations(knowledge_embs, 2):
                semdis = compute_sem_dis(emb1, emb2)
                if max_knowledge_semdis is None or semdis > max_knowledge_semdis:
                    max_knowledge_semdis = semdis
            sample["max_knowledge_semdis"] = max_knowledge_semdis
        else:
            sample["max_knowledge_semdis"] = 0
    return {"max_knowledge_semdis": mean([sample["max_knowledge_semdis"] for sample in data])}

def compute_usage_and_cost(input_data, source_data_dict=None, **kwargs):
    model = input_data["metadata"]["model_name"]
    data = input_data["data"]
    for sample in tqdm(data, desc="Computing usage and cost"):
        source_sample = source_data_dict.get(sample["id"], {}) if source_data_dict else {}
        usage, cost = compute_usage({**sample, **source_sample}, model=model)
        sample["usage"] = usage
        sample["cost"] = cost
    return {
        "usage": {
            "input_tokens": sum([sample["usage"]["input_tokens"] for sample in data if sample.get("usage")]),
            "output_tokens": sum([sample["usage"]["output_tokens"] for sample in data if sample.get("usage")]),
            "total_tokens": sum([sample["usage"]["total_tokens"] for sample in data if sample.get("usage")])
        },
        "cost": {
            "input": sum([sample["cost"]["input"] for sample in data if sample.get("cost")]),
            "output": sum([sample["cost"]["output"] for sample in data if sample.get("cost")]),
            "total": sum([sample["cost"]["total"] for sample in data if sample.get("cost")])
        }
    }

def compute_benchmark_contamination(input_data, source_data_dict=None, **kwargs):
    data = input_data["data"]
    rouge = evaluate.load("rouge")
    bleurt = evaluate.load("bleurt", config_name="BLEURT-20")
    for sample in tqdm(data, desc="Computing benchmark contamination"):
        source_sample = source_data_dict.get(sample["id"], {}) if source_data_dict else {}
        rouge_scores = rouge.compute(predictions=[sample["output"]], references=[source_sample["q_suffix"]], rouge_types=["rougeL"])
        rouge_l_score = rouge_scores["rougeL"]
        sample["rouge_l_score"] = rouge_l_score
        bleurt_scores = bleurt.compute(predictions=[sample["output"]], references=[source_sample["q_suffix"]])
        bleurt_score = bleurt_scores["scores"][0]
        sample["bleurt_score"] = bleurt_score
    return {"rouge_l_score": mean([sample["rouge_l_score"] for sample in data]), "bleurt_score": mean([sample["bleurt_score"] for sample in data])}

def compute_benchmark_contamination_by_quiz_mcq(input_data, source_data_dict=None, **kwargs):
    data = input_data["data"]

    for sample in tqdm(data, desc="Computing benchmark contamination"):
        source_sample = source_data_dict.get(sample["id"], {}) if source_data_dict else {}
        correct = sample["output"][0].strip().lower() == source_sample["correct_option"].strip() if sample["output"] else False
        sample["correct"] = correct

    return {"accuracy": mean([sample["correct"] for sample in data])}

def compute_benchmark_contamination_quiz_bdq_pos_bias(input_data, **kwargs):
    data = input_data["data"]
    pos_counter = Counter()

    for sample in tqdm(data, desc="Computing benchmark contamination"):
        pos_counter[sample["output"][0].strip().lower()] += 1

    return {"pos_freqs": dict(pos_counter)}

METRIC_MAP = {
    "domain_semdis": compute_domain_semdis,
    "max_domain_semdis": compute_max_domain_semdis,
    "knowledge_semdis": compute_knowledge_semdis,
    "max_knowledge_semdis": compute_max_knowledge_semdis,
    "usage_and_cost": compute_usage_and_cost,
    "benchmark_contamination": compute_benchmark_contamination,
    "benchmark_contamination_by_quiz_mcq": compute_benchmark_contamination_by_quiz_mcq,
    "benchmark_contamination_quiz_bdq_pos_bias": compute_benchmark_contamination_quiz_bdq_pos_bias
}

def report_metrics(data_files, metric=None, source_datapath=None):
    for data_file in tqdm(data_files, total=len(data_files), desc="Computing metrics"):
        input_data = read_json(data_file)
        if "data" in input_data:
            source_data_dict = {}
            if source_datapath:
                source_data = read_json(source_datapath)
                source_data_dict = {item["id"]: item for item in source_data["data"]}
            metrics = METRIC_MAP[metric](input_data, source_data_dict=source_data_dict)
            if "metrics" not in input_data:
                input_data["metrics"] = {}
            input_data["metrics"].update(metrics)
            write_json(input_data, data_file)

def main():
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-paths", nargs="+", type=str, help="Path(s) to data", required=True)
    parser.add_argument("-m", "--metric", type=str, default="domain_semdis", help="Metric name")
    parser.add_argument("--source-datapath", type=str, help="Path to source task data in json")

    args = parser.parse_args()

    files_to_process = []
    for data_path in args.data_paths:
        results_path = pathlib.Path(data_path)
        if results_path.is_file():
            files_to_process.append(data_path)
        else:
            files_to_process.extend(find_files(data_path))

    report_metrics(files_to_process, metric=args.metric, source_datapath=args.source_datapath)


if __name__ == "__main__":
    main()
