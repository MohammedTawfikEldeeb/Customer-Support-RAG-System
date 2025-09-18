import json
from src import config

def load_json(filename: str) -> list:
    with open(config.DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)