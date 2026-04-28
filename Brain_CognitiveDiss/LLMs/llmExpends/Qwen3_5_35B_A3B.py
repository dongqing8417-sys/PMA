import os
from openai import OpenAI


class QWen:
    def __init__(self):
        self.model = os.getenv("DASHSCOPE_QWEN_MODEL", "qwen3-35b-a3b")
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise RuntimeError("Missing DASHSCOPE_API_KEY environment variable.")
        self.client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        )

    def ask(self, prompt):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
