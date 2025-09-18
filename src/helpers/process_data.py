from src.ingestion.data_loader import load_json
from src.processing.chunking import format_menu_chunk, format_branch_chunk, format_note_chunk
from src import config
import json


all_documents = []

datasets = {
    "menu": ("menu.json", format_menu_chunk),
    "branches": ("branches.json", format_branch_chunk),
    "notes": ("notes.json", format_note_chunk)
}

for name, (filename, formatter) in datasets.items():
    data = load_json(filename)
    for idx, item in enumerate(data, start=1):
        all_documents.append(formatter(item, idx))

with open(config.PROCESSED_DATA_DIR / "all_documents.json", "w", encoding="utf-8") as f:
    json.dump(all_documents, f, indent=2, ensure_ascii=False)

print(f"Processed {len(all_documents)} documents!")
