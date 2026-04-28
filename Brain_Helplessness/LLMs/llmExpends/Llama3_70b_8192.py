import os
from openai import OpenAI


class Llama3:
    def __init__(self):
        self.model = os.getenv("DEEPINFRA_LLAMA_MODEL", "meta-llama/Meta-Llama-3-70B-Instruct")
        api_key = os.getenv("DEEPINFRA_API_KEY")
        if not api_key:
            raise RuntimeError("Missing DEEPINFRA_API_KEY environment variable.")
        self.client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("DEEPINFRA_BASE_URL", "https://api.deepinfra.com/v1/openai"),
        )

    def ask(self, prompt, temperature=1):
        result = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return result.choices[0].message.content
