# Prepare Transformer Dataset
# Purpose: prepare grievance dataset for AraBERT and DarijaBERT classification

import json
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = BASE_DIR / "data" / "test_datasets" / "test_dataset_darija.jsonl"
OUTPUT_DIR = BASE_DIR / "data" / "prepared_transformer_dataset"

TRAIN_PATH = OUTPUT_DIR / "train.jsonl"
TEST_PATH = OUTPUT_DIR / "test.jsonl"
LABEL_MAP_PATH = OUTPUT_DIR / "label_map.json"


RANDOM_SEED = 42
TRAIN_RATIO = 0.8


def load_jsonl(path):
    rows = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))

    return rows


def get_text(row):
    if "text" in row:
        return row["text"]

    if "transcript" in row:
        return row["transcript"]

    if "complaint" in row:
        return row["complaint"]

    raise KeyError("Could not find text field in row.")


def get_label(row):
    if "expected_category" in row:
        return row["expected_category"]

    if "category" in row:
        return row["category"]

    if "label" in row:
        return row["label"]

    raise KeyError("Could not find category label field in row.")


def normalize_row(row):
    return {
        "id": row.get("id"),
        "text": get_text(row),
        "label": get_label(row),
        "urgency": row.get("expected_urgency", row.get("urgency")),
        "language": row.get("language", "darija")
    }


def save_jsonl(rows, path):
    with open(path, "w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_rows = load_jsonl(INPUT_PATH)
    rows = [normalize_row(row) for row in raw_rows]

    labels = sorted(set(row["label"] for row in rows))
    label_to_id = {label: index for index, label in enumerate(labels)}
    id_to_label = {index: label for label, index in label_to_id.items()}

    for row in rows:
        row["label_id"] = label_to_id[row["label"]]

    random.seed(RANDOM_SEED)
    random.shuffle(rows)

    split_index = int(len(rows) * TRAIN_RATIO)

    train_rows = rows[:split_index]
    test_rows = rows[split_index:]

    save_jsonl(train_rows, TRAIN_PATH)
    save_jsonl(test_rows, TEST_PATH)

    with open(LABEL_MAP_PATH, "w", encoding="utf-8") as file:
        json.dump(
            {
                "label_to_id": label_to_id,
                "id_to_label": id_to_label,
                "num_labels": len(labels)
            },
            file,
            ensure_ascii=False,
            indent=2
        )

    print("=" * 80)
    print("Transformer Dataset Preparation")
    print("=" * 80)
    print(f"Input examples: {len(rows)}")
    print(f"Training examples: {len(train_rows)}")
    print(f"Testing examples: {len(test_rows)}")
    print(f"Number of labels: {len(labels)}")
    print(f"Labels: {labels}")
    print(f"Train file saved to: {TRAIN_PATH}")
    print(f"Test file saved to: {TEST_PATH}")
    print(f"Label map saved to: {LABEL_MAP_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()
