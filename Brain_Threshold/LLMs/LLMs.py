from LLMs.llmExpends.Llama3_70b_8192 import Llama3_70b_8192
from LLMs.llmExpends.Qwen3_5_35B_A3B import Qwen3_5_35B_A3B
from LLMs.llmExpends.DeepSeek_V3_2 import DeepSeek_V3_2
from LLMs.llmExpends.GLM4_5_Air import GLM4_5_Air


MODEL_ALIASES = {
    "Llama-3-70B-Instruct": "llama",
    "llama3-70b-8192": "llama",
    "llama3-70b-instruct": "llama",
    "Qwen3.5-35B-A3B": "qwen",
    "qwen1.5-72b": "qwen",
    "qwen3.5-flash": "qwen",
    "DeepSeek-V3.2": "deepseek",
    "deepseek-v3.2": "deepseek",
    "GLM-4.5-Air": "glm",
    "glm4-flash": "glm",
    "glm-4.7-flash": "glm",
    "glm-4.5-air": "glm",
}

DEFAULT_JSON_MODEL = "Llama-3-70B-Instruct"


class LLMs:
    def __init__(self, model, prompt):
        self.model = model
        self.prompt = prompt

    def ask(self, is_json=False):
        model_key = MODEL_ALIASES.get(self.model, MODEL_ALIASES.get(DEFAULT_JSON_MODEL))
        if model_key == "llama":
            return Llama3_70b_8192(self.prompt).generate_response(is_json=is_json)
        if model_key == "qwen":
            return Qwen3_5_35B_A3B(self.prompt).generate_response(is_json=is_json)
        if model_key == "deepseek":
            return DeepSeek_V3_2(self.prompt).generate_response(is_json=is_json)
        if model_key == "glm":
            return GLM4_5_Air(self.prompt).generate_response(is_json=is_json)
        raise ValueError(f"Unsupported model: {self.model}")
