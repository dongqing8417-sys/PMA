from pathlib import Path


class Prompt:
    def __init__(self, filename):
        prompt_dir = Path(__file__).resolve().parent
        self.file_path = prompt_dir / f"{filename}.txt"

    def read(self):
        with self.file_path.open("r", encoding="utf-8") as file:
            return file.read()

    def to_string(self, params):
        template = self.read()
        for key, value in params.items():
            template = template.replace("{" + key + "}", str(value))
            template = template.replace(key if key.startswith("{") else "{" + key + "}", str(value))
        return template
