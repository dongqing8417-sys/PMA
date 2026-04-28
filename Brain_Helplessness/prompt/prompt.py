from datetime import datetime, time
from pathlib import Path
from typing import Any, Dict
import json

PROMPT_DIR = Path(__file__).resolve().parent


class Prompt:
    def __init__(self, part: str):
        self.text = ""
        self.part = part
        self.load_text(part)

    def cover(self, text: str) -> None:
        self.text = text

    def to_string(self, params: Dict[str, Any]) -> str:
        text = self.text
        for key, value in params.items():
            key = str(key)

            if not isinstance(value, str):
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
                elif isinstance(value, time):
                    value = value.strftime("%H:%M")
                elif isinstance(value, datetime):
                    value = value.strftime("%Y-%m-%d %H:%M")
                else:
                    value = str(value)

            text = text.replace(key, value)

        return text

    def load_text(self, name: str) -> None:
        prompt_path = PROMPT_DIR / f"{name}.txt"
        with prompt_path.open("r", encoding="utf-8") as text_file:
            self.text = text_file.read()
