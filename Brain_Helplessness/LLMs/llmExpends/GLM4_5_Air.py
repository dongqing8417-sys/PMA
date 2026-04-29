import os
from openai import OpenAI


class GLM4Air:
    def __init__(self):
        self.model = os.getenv("ZHIPU_MODEL", "glm-4.5-air")
        api_key = os.getenv("ZHIPU_API_KEY")
        if not api_key:
            raise RuntimeError("Missing ZHIPU_API_KEY environment variable.")
        self.client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4"),
        )

    def ask(self, prompt):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "AI"},
                {"role": "user", "content": prompt},
            ],
            temperature=1,
        )
        return completion.choices[0].message.content
