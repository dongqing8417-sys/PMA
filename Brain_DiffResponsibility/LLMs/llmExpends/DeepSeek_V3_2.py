import os
from openai import OpenAI

class DeepSeek_V3_2:
    def __init__(self, prompt):
        self.prompt = prompt
        self.base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        self.api_key = os.getenv("DEEPSEEK_API_KEY", "")
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    def generate_response(self, is_json=False):
        client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        kwargs = {"model": self.model, "messages": [{"role": "user", "content": self.prompt}], "temperature": 0.7}
        if is_json:
            kwargs["response_format"] = {"type": "json_object"}
        response = client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content
        if is_json:
            import json
            return json.loads(content)
        return content
