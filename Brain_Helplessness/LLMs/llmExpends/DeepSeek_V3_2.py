import os
from openai import OpenAI


class DeepSeek:
    def __init__(self):
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-v3.2")
        api_key = os.getenv("VOLCENGINE_API_KEY")
        if not api_key:
            raise RuntimeError("Missing VOLCENGINE_API_KEY environment variable.")
        self.client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("VOLCENGINE_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"),
        )

    def ask(self, prompt):
        response = self.client.responses.create(
            model=self.model,
            input=[{"role": "user", "content": prompt}],
        )
        return response.output_text
