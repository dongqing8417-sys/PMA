import json
import random
import re
import time
from typing import Any, Optional

DEFAULT_JSON_MODEL = "Llama-3-70B-Instruct"


class LLMs:
    def __init__(self, model_name, prompt, max_retries=5, backoff_factor=0.5):
        self.model_name = model_name
        self.model = self._get_model(model_name)
        self.prompt = prompt
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def _get_model(self, model_name):
        if model_name in {"Llama-3-70B-Instruct", "llama3-70b-8192", "llama3-70b-instruct"}:
            from LLMs.llmExpends.Llama3_70b_8192 import Llama3
            return Llama3()
        if model_name in {"Qwen3.5-35B-A3B", "qwen3.5-flash"}:
            from LLMs.llmExpends.Qwen3_5_35B_A3B import QWen
            return QWen()
        if model_name in {"DeepSeek-V3.2", "deepseek-v3.2"}:
            from LLMs.llmExpends.DeepSeek_V3_2 import DeepSeek
            return DeepSeek()
        if model_name in {"GLM-4.5-Air", "glm-4.7-flash", "glm-4.5-air"}:
            from LLMs.llmExpends.GLM4_5_Air import GLM4Air
            return GLM4Air()
        raise ValueError(f"Unsupported model: {model_name}")

    def ask(self, to_json=False):
        last_error: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.model.ask(self.prompt)
                if not to_json:
                    return response
                return self._parse_json_response(response)
            except Exception as exc:
                last_error = exc
                if attempt == self.max_retries:
                    break
                wait_time = self.backoff_factor * (2 ** (attempt - 1))
                time.sleep(wait_time + random.uniform(0, 0.1 * wait_time))
        raise RuntimeError(f"Failed after {self.max_retries} attempts: {last_error}")

    def _parse_json_response(self, response: Any):
        if isinstance(response, (list, dict)):
            return response

        text = str(response).strip()
        candidates = [text, self._strip_code_fence(text), self._extract_json_block(text)]
        for candidate in candidates:
            if not candidate:
                continue
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                continue

        repair_prompt = (
            "Convert the following text into valid JSON for json.loads(). "
            "Return JSON only, with no explanation:\n" + text
        )
        repaired = self.__class__(DEFAULT_JSON_MODEL, repair_prompt).ask(to_json=False)
        repaired_text = self._extract_json_block(self._strip_code_fence(str(repaired).strip()))
        return json.loads(repaired_text)

    def _strip_code_fence(self, text: str) -> str:
        if text.startswith("```"):
            text = re.sub(r"^```[a-zA-Z0-9_-]*\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
        return text.strip()

    def _extract_json_block(self, text: str) -> str:
        match = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
        return match.group(1).strip() if match else text.strip()
