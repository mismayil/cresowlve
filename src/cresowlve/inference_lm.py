import argparse
import math
from openai import AsyncOpenAI, AsyncAzureOpenAI, APITimeoutError, APIConnectionError, RateLimitError, InternalServerError, BadRequestError
import os
from tqdm import tqdm
import pathlib
from abc import ABC, abstractmethod
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import asyncio, dataclasses
from dotenv import load_dotenv
import logging, sys
from google import genai
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable, DeadlineExceeded
from google.genai import types as genai_types
from anthropic import (AsyncAnthropic, RateLimitError as AnthropicRateLimitError, APIConnectionError as AnthropicAPIConnectionError, 
                       APITimeoutError as AnthropicAPITimeoutError, InternalServerError as AnthropicInternalServerError)

logging.basicConfig(stream=sys.stderr, level=logging.WARN)
logger = logging.getLogger(__name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

from cresowlve.utils import read_json, write_json, generate_unique_id, generate_datetime_id, batched, none_or_int, none_or_str

TOGETHER_MODELS = []
RCP_AI_MODELS = ["Qwen/Qwen3.5-397B-A17B", "meta-llama/Llama-3.3-70B-Instruct", "Qwen/Qwen3-235B-A22B-Thinking-2507", "zai-org/GLM-5",
                 "allenai/OLMo-2-0325-32B-Instruct", "deepseek-ai/DeepSeek-V3.2", "swiss-ai/Apertus-70B-Instruct-2509",
                 "Qwen/Qwen3-235B-A22B-Instruct-2507", "mistralai/Mistral-Large-3-675B-Instruct-2512", "CohereLabs/c4ai-command-a-03-2025"]
HF_API_MODELS = []

def is_thinking_model(model_name):
    return model_name.startswith("gpt-5") or model_name.startswith("gemini-2.5") or model_name.startswith("gemini-3")

@dataclasses.dataclass
class ModelResponse:
    sample_id: str = None
    text: str = None
    usage: dict = None
    exception: Exception = None
    thoughts: str = None

class InferenceService(ABC):
    @abstractmethod
    async def generate(self, batch, **kwargs):
        pass

    @abstractmethod
    def prepare_model_args(self, model_args, **kwargs):
        pass

class OpenAIService(InferenceService):
    def __init__(self, model_name, api_key, model_args=None, api_version=None, api_endpoint=None):
        self.model_name = model_name
        self.api_key = api_key
        self.model_args = model_args
        self.api_version = api_version
        self.api_endpoint = api_endpoint
        self.client = self.init_client()
        self.config = self.prepare_model_args(model_args)

    def init_client(self):
        openai_azure = self.api_endpoint is not None or os.getenv("AZURE_OPENAI_API_ENDPOINT") is not None
        if openai_azure:
            endpoint = self.api_endpoint if self.api_endpoint is not None else os.getenv("AZURE_OPENAI_API_ENDPOINT")
            client = AsyncAzureOpenAI(
                api_key = self.api_key if self.api_key is not None else os.getenv("AZURE_OPENAI_API_KEY"),
                api_version = self.api_version if self.api_version is not None else os.getenv("AZURE_OPENAI_API_VERSION"),
                azure_endpoint=endpoint
            )
        else:
            client = AsyncOpenAI(api_key=self.api_key if self.api_key is not None else os.getenv("OPENAI_API_KEY"))
        return client

    def prepare_model_args(self, model_args):
        if not model_args:
            return {}

        if self.model_name and is_thinking_model(self.model_name):
            out = {}
            if model_args.get("max_tokens") is not None:
                out["max_output_tokens"] = model_args["max_tokens"]
            
            thinking = {}

            if model_args.get("enable_thinking_summary", False):
                thinking["summary"] = "auto"
            
            thinking_effort = model_args.get("enable_thinking_effort")
            if thinking_effort:
                if thinking_effort in ["minimal", "low", "medium", "high"]:
                    thinking["effort"] = thinking_effort
                else:
                    raise ValueError(f"Invalid thinking effort level: {model_args.get('enable_thinking_effort')}")
            
            out["reasoning"] = thinking
            return out

        # Other models
        out = {}
        if model_args.get("temperature") is not None:
            out["temperature"] = model_args["temperature"]
        if model_args.get("top_p") is not None:
            out["top_p"] = model_args["top_p"]
        if model_args.get("max_tokens") is not None:
            out["max_tokens"] = model_args["max_tokens"]
        
        return out
    
    def _extract_text_and_thoughts_from_response(self, response):
        text = getattr(response, "output_text", None)
        thoughts = None

        text_parts = []
        thinking_parts = []
        try:
            for item in getattr(response, "output", []):
                summaries = getattr(item, "summary", []) or []
                contents = getattr(item, "content", []) or []
                for c in summaries + contents:
                    t = getattr(c, "text", None)
                    if not t and isinstance(c, dict):
                        t = c.get("text")
                    if t:
                        ctype = getattr(c, "type", None)
                        if ctype == "summary_text":
                            thinking_parts.append(t)
                        else:
                            text_parts.append(t)
            if thinking_parts:
                thoughts = "\n".join(thinking_parts).strip()
            if text_parts:
                text = "\n".join(text_parts).strip()
            if text or thoughts:
                return text, thoughts
        except Exception as e:
            print(response)
            raise e

        if getattr(response, "choices", None):
            msg = response.choices[0].message
            cont = getattr(msg, "content", "")
            if isinstance(cont, list):
                return "".join(seg.get("text", "") for seg in cont if isinstance(seg, dict)).strip(), thoughts
            elif isinstance(cont, str):
                if cont.strip():
                    return cont.strip(), thoughts

        return text, thoughts
    
    def _extract_exception_from_response(self, response):
        choices = getattr(response, "choices", None)
        if choices and len(choices) > 0:
            finish_reason = getattr(choices[0], "finish_reason", None)
            if finish_reason and finish_reason != "stop":
                return f"Finish reason: {finish_reason}"
        code = getattr(response, 'code', None)
        message = getattr(response, 'message', None)
        if code or message:
            return f"code: {code}, message: {message}"
        return None

    def _extract_usage_from_response(self, response):
        prompt_tokens = getattr(response.usage, "prompt_tokens", None)
        completion_tokens = getattr(response.usage, "completion_tokens", None)

        if prompt_tokens is not None and completion_tokens is not None:
            return {
                "input_tokens": prompt_tokens,
                "output_tokens": completion_tokens,
            }

        return {
            "input_tokens": getattr(response.usage, "input_tokens", None),
            "output_tokens": getattr(response.usage, "output_tokens", None),
            "thinking_tokens": getattr(getattr(response.usage, "output_tokens_details", None), "reasoning_tokens", None)
        }

    @retry(
            retry=retry_if_exception_type((APITimeoutError, APIConnectionError, RateLimitError, InternalServerError)), 
            wait=wait_random_exponential(min=1, max=60), 
            stop=stop_after_attempt(3), 
            before_sleep=before_sleep_log(logger, logging.DEBUG)
    )
    async def chat_completion(self, sample_id, messages):
        try:
            response = await self.client.chat.completions.create(model=self.model_name, messages=messages, **self.config)
            text, thoughts = self._extract_text_and_thoughts_from_response(response)
            exception = self._extract_exception_from_response(response)
            usage = self._extract_usage_from_response(response)
        except Exception as e:
            text = ""
            usage = {}
            thoughts = None
            exception = str(e)

        return ModelResponse(sample_id=sample_id, text=text, thoughts=thoughts, usage=usage, exception=exception)

    @retry(
        retry=retry_if_exception_type((APITimeoutError, APIConnectionError, RateLimitError, InternalServerError)),
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(3),
        before_sleep=before_sleep_log(logger, logging.DEBUG),
    )
    async def responses_api(self, sample_id, user_prompt, system_prompt=None):
        try:
            response = await self.client.responses.create(model=self.model_name, input=user_prompt, instructions=system_prompt, **self.config)
            text, thoughts = self._extract_text_and_thoughts_from_response(response)
            exception = self._extract_exception_from_response(response)
            usage = self._extract_usage_from_response(response)
        except Exception as e:
            text = ""
            thoughts = None
            usage = {}
            exception = str(e)
    
        return ModelResponse(sample_id=sample_id, text=text, thoughts=thoughts, usage=usage, exception=exception)

    async def generate(self, batch):
        tasks = []
        for sample in batch:
            user_prompt = sample["user_prompt"]
            system_prompt = sample.get("system_prompt")
            sample_id = sample["id"]
            tasks.append(asyncio.create_task(self.responses_api(sample_id, user_prompt, system_prompt=system_prompt)))
        return await asyncio.gather(*tasks)

class OpenAICompatibleService(OpenAIService):
    async def generate(self, batch):
        tasks = []
        for sample in batch:
            user_prompt = sample["user_prompt"]
            system_prompt = sample.get("system_prompt")
            sample_id = sample["id"]
            messages = []
            if system_prompt and system_prompt.strip():
                messages.append({"role": "system", "content": system_prompt.strip()})
            messages.append({"role": "user", "content": user_prompt.strip()})
            tasks.append(asyncio.create_task(self.chat_completion(sample_id, messages)))
        return await asyncio.gather(*tasks)

class TogetherService(OpenAICompatibleService):
    def init_client(self):
        return AsyncOpenAI(base_url="https://api.together.xyz/v1", api_key=self.api_key if self.api_key is not None else os.getenv("TOGETHER_API_KEY"))
    
class HFAPIService(OpenAICompatibleService):
    def init_client(self):
        return AsyncOpenAI(base_url="https://api-inference.huggingface.co/v1/", api_key=self.api_key if self.api_key is not None else os.getenv("HF_API_KEY"))

class RCPAIService(OpenAICompatibleService):
    def init_client(self):
        return AsyncOpenAI(base_url="https://inference.rcp.epfl.ch/v1", api_key=self.api_key if self.api_key is not None else os.getenv("RCP_AI_API_KEY"))
    
class AnthropicService(InferenceService):
    def __init__(self, model_name, api_key, model_args=None):
        self.model_name = model_name
        self.api_key = api_key
        self.config = self.prepare_model_args(model_args)
        self.client = self.init_client()

    def init_client(self):
        return AsyncAnthropic(api_key=self.api_key if self.api_key is not None else os.getenv("ANTHROPIC_API_KEY"))

    def prepare_model_args(self, model_args, **kwargs):
        anthropic_model_args = {}
        if model_args is not None:
            if model_args.get("temperature") is not None:
                anthropic_model_args["temperature"] = model_args["temperature"]
            if model_args.get("max_tokens") is not None:
                anthropic_model_args["max_tokens"] = model_args["max_tokens"]
            if model_args.get("top_p") is not None:
                anthropic_model_args["top_p"] = model_args["top_p"]
            if model_args.get("top_k") is not None:
                anthropic_model_args["top_k"] = model_args["top_k"]
            
            thinking_config = {}

            if model_args.get("enable_thinking_summary", False):
                thinking_config["thinking"] = {"type": "adaptive"}
            
            thinking_effort = model_args.get("enable_thinking_effort")
            if thinking_effort:
                if thinking_effort in ["low", "medium", "high", "max"]:
                    thinking_config["output_config"] = {"effort": thinking_effort}
                else:
                    raise ValueError(f"Invalid thinking effort level: {model_args.get('enable_thinking_effort')}")
            anthropic_model_args.update(thinking_config)
        return anthropic_model_args

    def _extract_text_and_thoughts_from_response(self, response):
        text = ""
        thoughts = ""

        text_parts = []
        thinking_parts = []

        for c in getattr(response, "content", []):
            ctype = getattr(c, "type", None)
            text = getattr(c, "text", "").strip()
            if ctype == "text":
                text_parts.append(text)
            elif ctype == "thinking":
                thinking_parts.append(text)
        if text_parts:
            text = "\n".join(text_parts).strip()
        if thinking_parts:
            thoughts = "\n".join(thinking_parts).strip()
        
        return text, thoughts

    def _extract_exception_from_response(self, response):
        stop_reason = getattr(response, "stop_reason", None)
        if stop_reason is not None and stop_reason != "end_turn":
            return f"Stop reason: {stop_reason}"
        return None
    
    def _extract_usage_from_response(self, response):
        usage = {}
        try:
            usage["input_tokens"] = getattr(response.usage, "input_tokens", None)
            usage["output_tokens"] = getattr(response.usage, "output_tokens", None)
        except Exception:
            pass
        return usage

    @retry(
        retry=retry_if_exception_type((AnthropicAPITimeoutError, AnthropicAPIConnectionError, AnthropicRateLimitError, AnthropicInternalServerError)), 
        wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3), before_sleep=before_sleep_log(logger, logging.DEBUG)
    )
    async def chat_completion(self, sample_id, messages, system_prompt=None):
        try:
            config = self.config
            if system_prompt and system_prompt.strip():
                config["system"] = system_prompt.strip()
            response = await self.client.messages.create(model=self.model_name, messages=messages, **config)
            text, thoughts = self._extract_text_and_thoughts_from_response(response)
            exception = self._extract_exception_from_response(response)
            usage = self._extract_usage_from_response(response)
        except Exception as e:
            text = ""
            thoughts = ""
            usage = {}
            exception = str(e)
        
        return ModelResponse(sample_id=sample_id, text=text, thoughts=thoughts, usage=usage, exception=exception)

    async def generate(self, batch):
        tasks = []
        for sample in batch:
            user_prompt = sample["user_prompt"]
            system_prompt = sample.get("system_prompt")
            sample_id = sample["id"]
            tasks.append(asyncio.create_task(self.chat_completion(sample_id, [{"role": "user", "content": user_prompt.strip()}], system_prompt=system_prompt)))
        return await asyncio.gather(*tasks)

class GoogleService(InferenceService):
    def __init__(self, model_name, api_key, model_args=None):
        self.model_name = model_name
        self.api_key = api_key
        self.config = self.prepare_model_args(model_args)
        self.client = self.init_client()

    def init_client(self):
        return genai.Client(api_key=self.api_key if self.api_key is not None else os.getenv("GOOGLE_API_KEY"))

    def prepare_model_args(self, model_args):
        cfg = {}

        if model_args is not None:
            temp = model_args.get("temperature")
            if temp is not None and not is_thinking_model(self.model_name):
                cfg["temperature"] = temp

            max_tok = model_args.get("max_tokens")
            if max_tok is not None:
                # GenAI SDK uses max_output_tokens
                cfg["max_output_tokens"] = max_tok

            top_p = model_args.get("top_p")
            if top_p is not None:
                cfg["top_p"] = top_p

            top_k = model_args.get("top_k")
            if top_k is not None:
                cfg["top_k"] = top_k

            thinking_cfg = {"include_thoughts": model_args.get("enable_thinking_summary", False)}
            thinking_effort = model_args.get("enable_thinking_effort")
            
            if thinking_effort:
                if thinking_effort in ["minimal", "low", "medium", "high"]:
                    if self.model_name.startswith("gemini-2"):
                        thinking_cfg["thinking_budget"] = -1
                    else:
                        thinking_cfg["thinking_level"] = thinking_effort
                else:
                    raise ValueError(f"Invalid thinking effort level: {model_args.get('enable_thinking_effort')}")
            
            cfg["thinking_config"] = genai_types.ThinkingConfig(**thinking_cfg)

        return cfg

    def _extract_text_and_thoughts_from_response(self, response):
        text = ""
        thoughts = ""

        try:
            text_parts = []
            thought_parts = []
            for cand in getattr(response, "candidates", []) or []:
                content = getattr(cand, "content", None)
                if not content:
                    continue
                for part in (getattr(content, "parts", []) or []):
                    thought = getattr(part, "thought", None)
                    txt = getattr(part, "text", None)
                    if isinstance(txt, str) and txt.strip():
                        if thought:
                            thought_parts.append(txt.strip())
                        else:
                            text_parts.append(txt.strip())
            if text_parts:
                text = "\n".join(text_parts).strip()
            if thought_parts:
                thoughts = "\n".join(thought_parts).strip()
        except Exception:
            pass
        return text, thoughts

    def _extract_exception_from_response(self, response):
        exception = None
        finish_reason = None
        safety_ratings = None

        try:
            cands = getattr(response, "candidates", None) or []
            if cands:
                fr = getattr(cands[0], "finish_reason", None)
                if fr is not None:
                    finish_reason = str(fr)

                sr = getattr(cands[0], "safety_ratings", None)
                if sr is not None:
                    safety_ratings = ",".join([str(x) for x in sr])
        except Exception:
            pass
        
        if finish_reason and finish_reason != "FinishReason.STOP":
            exception = f"Finish reason: {finish_reason}, safety ratings: {safety_ratings}"
        
        return exception

    def _extract_usage_from_response(self, response):
            usage = {}

            try:
                usage_metadata = getattr(response, "usage_metadata", None)
                if usage_metadata is not None:
                    usage["input_tokens"] = getattr(usage_metadata, "prompt_token_count", None)
                    usage["output_tokens"] = getattr(usage_metadata, "candidates_token_count", None)
                    usage["thinking_tokens"] = getattr(usage_metadata, "thoughts_token_count", None)
            except Exception:
                pass
            return usage

    @retry(
        retry=retry_if_exception_type((ResourceExhausted, ServiceUnavailable, DeadlineExceeded)),
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(3),
        before_sleep=before_sleep_log(logger, logging.DEBUG),
    )
    async def generate_content(self, sample_id, user_prompt, system_prompt=None):
        try:
            config = self.config

            if system_prompt and system_prompt.strip():
                config["system_instruction"] = system_prompt.strip()
            
            config = genai_types.GenerateContentConfig(**config)

            def _call():
                if config is not None:
                    return self.client.models.generate_content(
                        model=self.model_name,
                        contents=user_prompt.strip(),
                        config=config,
                    )
                else:
                    return self.client.models.generate_content(
                        model=self.model_name,
                        contents=user_prompt.strip(),
                    )

            response = await asyncio.to_thread(_call)

            text, thoughts = self._extract_text_and_thoughts_from_response(response)
            exception = self._extract_exception_from_response(response)
            usage = self._extract_usage_from_response(response)

            return ModelResponse(sample_id=sample_id, text=text, thoughts=thoughts, usage=usage, exception=exception)

        except Exception as e:
            return ModelResponse(sample_id=sample_id, text="", thoughts=None, usage=None, exception=str(e))

    async def generate(self, batch):
        tasks = []
        for sample in batch:
            user_prompt = sample["user_prompt"]
            system_prompt = sample.get("system_prompt")
            sample_id = sample["id"]
            tasks.append(asyncio.create_task(self.generate_content(sample_id, user_prompt, system_prompt=system_prompt)))
        return await asyncio.gather(*tasks)

class HFService(InferenceService):
    def __init__(self, model_name, model_args=None):
        self.model_path = model_name
        self.tokenizer_path = model_name
        self.model_name = model_name.split("/")[-1].lower()
        self.config = self.prepare_model_args(model_args)
        self.model, self.tokenizer = self.load_model()
    
    def load_model(self):
        tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)
        model = AutoModelForCausalLM.from_pretrained(self.model_path, 
                                                    device_map=device,
                                                    torch_dtype=torch.bfloat16)
        model.eval()
        return model, tokenizer

    def prepare_model_args(self, model_args):
        hf_model_args = {}

        if model_args is not None:
            if "temperature" in model_args:
                hf_model_args["temperature"] = model_args["temperature"]
            if "max_tokens" in model_args:
                hf_model_args["max_new_tokens"] = model_args["max_tokens"]
            if "top_p" in model_args:
                hf_model_args["top_p"] = model_args["top_p"]
            if "top_k" in model_args:
                hf_model_args["top_k"] = model_args["top_k"]
            if hf_model_args["top_p"] == 1 and not hf_model_args.get("top_k"):
                hf_model_args["do_sample"] = False
            else:
                hf_model_args["do_sample"] = True
        return hf_model_args

    async def generate(self, batch, model_args=None):
        self.tokenizer.padding_side = "left"

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        responses = []

        all_messages = []

        for sample in batch:
            messages = []

            if sample.get("system_prompt"):
                messages.append(
                    {"role": "system", "content": sample["system_prompt"].strip()}
                )

            messages.append({"role": "user", "content": sample["user_prompt"].strip()})
            all_messages.append(messages)
        
        inputs = self.tokenizer.apply_chat_template(
            all_messages,
            add_generation_prompt=True,
            padding="longest",
            return_tensors="pt",
            return_dict=True,
        ).to(device)

        outputs = self.model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            tokenizer=self.tokenizer,
            **self.config,
        )

        for i, (sample, output) in enumerate(zip(batch, outputs)):
            response = output[inputs["input_ids"].shape[-1] :]
            responses.append(
                ModelResponse(
                    sample_id=sample["id"],
                    text=self.tokenizer.decode(
                        response,
                        skip_special_tokens=True,
                        clean_up_tokenization_spaces=True,
                    )
                )
            )
        
        return responses

def get_inference_service(model_name, api_key=None, model_args=None):
    if model_name.startswith("gpt"):
        return OpenAIService(model_name, api_key, model_args=model_args)
    elif model_name.startswith("gemini"):
        return GoogleService(model_name, api_key, model_args=model_args)
    elif model_name.startswith("claude"):
        return AnthropicService(model_name, api_key, model_args=model_args)
    elif model_name in RCP_AI_MODELS:
        return RCPAIService(model_name, api_key, model_args=model_args)
    elif model_name in TOGETHER_MODELS:
        return TogetherService(model_name, api_key, model_args=model_args)
    elif model_name in HF_API_MODELS:
        return HFAPIService(model_name, api_key, model_args=model_args)
    else:
        return HFService(model_name, model_args=model_args)

async def main():
    load_dotenv() 

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datapath", type=str, help="Path to inference data in json", required=True)
    parser.add_argument("-a", "--api-key", type=str, help="Model API Key")
    parser.add_argument("-m", "--model", type=str, help="Model to use for inference")
    parser.add_argument("-t", "--temperature", type=float, help="Temperature for generation", default=1.0)
    parser.add_argument("-g", "--max-tokens", type=none_or_int, help="Max tokens for generation", default=None)
    parser.add_argument("-p", "--top-p", type=float, help="Top-p for generation", default=None)
    parser.add_argument("-k", "--top-k", type=none_or_int, help="Top-k for generation", default=None)
    parser.add_argument("-fp", "--frequency-penalty", type=float, help="Frequency penalty for generation", default=0)
    parser.add_argument("-pp", "--presence-penalty", type=float, help="Presence penalty for generation", default=0)
    parser.add_argument("-o", "--output-dir", type=str, help="Output directory for inference results", default="outputs")
    parser.add_argument("-n", "--num-samples", type=int, help="Number of samples to run inference on", default=0)
    parser.add_argument("-b", "--batch-size", type=int, help="Batch size for inference", default=16)
    parser.add_argument("-r", "--resume-from-path", type=str, help="Resume inference from this path")
    parser.add_argument("-s", "--stop", type=none_or_str, help="Stop token for generation", default=None)
    parser.add_argument("--enable-thinking-summary", action="store_true", help="Whether to enable thinking summary in reasoning models")
    parser.add_argument("--enable-thinking-effort", type=none_or_str, choices=["minimal", "low", "medium", "high"], default=None, help="Effort level for thinking in reasoning models")
    
    args = parser.parse_args()
        
    input_data = read_json(args.datapath)
    data = input_data["data"]

    if args.resume_from_path:
        print("Resuming...")
        outputs = read_json(args.resume_from_path)
        outputs["data"] = [s for s in outputs["data"] if s["output"] and not s["exception"]]
        if args.max_tokens is not None:
            outputs["metadata"]["model_args"]["max_tokens"] = args.max_tokens
        resume_from_data_ids = [s["id"] for s in outputs["data"]]
        data = [s for s in data if s["id"] not in resume_from_data_ids]
        print(f"Found {len(data)} unfinished samples.")
        output_path = args.resume_from_path
    else:
        print("Starting a fresh run...")
        pathlib.Path(args.output_dir).mkdir(parents=True, exist_ok=True)
        datapath = pathlib.Path(args.datapath)
        model_name = args.model.split("/")[-1].lower()
        stop_token = args.stop.replace("\\n", "\n") if args.stop else None
        datetime_id = generate_datetime_id()
        output_path = os.path.join(args.output_dir, f"{datapath.stem}_{model_name}_{datetime_id}.json")

        outputs = {
            "metadata": {
                "source": args.datapath,
                "output_path": output_path,
                "size": len(data),
                "model": args.model,
                "model_name": model_name,
                "batch_size": args.batch_size,
                "num_samples": args.num_samples,
                "model_args": {
                    "temperature": args.temperature,
                    "max_tokens": args.max_tokens,
                    "top_p": args.top_p,
                    "top_k": args.top_k,
                    "frequency_penalty": args.frequency_penalty,
                    "presence_penalty": args.presence_penalty,
                    "stop": stop_token,
                    "enable_thinking_summary": args.enable_thinking_summary,
                    "enable_thinking_effort": args.enable_thinking_effort,
                }
            },
            "metrics": {},
            "data": [],
        }

    if args.num_samples > 0:
        print(f"Limiting to {args.num_samples} samples...")
        data = data[: args.num_samples]

    print(f"Writing to {output_path}")

    # check all data have sample ids
    for sample in data:
        if "id" not in sample:
            raise ValueError(f"Sample {sample} does not have an id")

    service = get_inference_service(args.model, args.api_key, model_args=outputs["metadata"]["model_args"])

    for batch in tqdm(batched(data, size=args.batch_size),
                      total=math.ceil(len(data) / args.batch_size)):
        responses = await service.generate(batch)

        for response in responses:
            sample = {
                "id": response.sample_id,
                "output": response.text,
                "thoughts": response.thoughts,
                "usage": response.usage,
                "exception": str(response.exception) if response.exception else None,
                "result_id": generate_unique_id()
            }
            outputs["data"].append(sample)

        write_json(outputs, output_path)

    write_json(outputs, output_path)

if __name__ == "__main__":
    asyncio.run(main())