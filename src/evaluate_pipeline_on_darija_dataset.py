# Evaluate Categorization + Routing Pipeline on Darija Dataset
# Purpose: run the pipeline on the Darija complaint test dataset

import json
from pathlib import Path

from grievance_categorization_routing_pipeline import process_grievance


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data" / "test_datasets" / "test_dataset_darija.jsonl"
OUTPUT_PATH = BASE_DIR / "tests" / "pipeline_darija_dataset_results_v1.jsonl"


def load_jsonl(path):
    rows = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))

    return rows


def get_text(item):
    if "text" in item:
        return item["text"]

    if "transcript" in item:
        return item["transcript"]

    if "complaint" in item:
        return item["complaint"]

    raise KeyError("No text/transcript/complaint field found in dataset row.")


def get_expected_category(item):
    if "expected_category" in item:
        return item["expected_category"]

    if "category" in item:
        return item["category"]

    if "label" in item:
        return item["label"]

    return None


def evaluate():
    dataset = load_jsonl(DATASET_PATH)

    total = 0
    correct_category = 0
    unknown_expected = 0
    results = []

    for item in dataset:
        total += 1

        transcript = get_text(item)
        expected_category = get_expected_category(item)

        pipeline_output = process_grievance(transcript)

        predicted_category = pipeline_output["routing_category_id"]

        if expected_category is None:
            category_correct = None
            unknown_expected += 1
        else:
            category_correct = predicted_category == expected_category

            if category_correct:
                correct_category += 1

        result_row = {
            "id": item.get("id", total),
            "text": transcript,
            "language": item.get("language", "darija"),
            "expected_category": expected_category,
            "predicted_category": predicted_category,
            "category_correct": category_correct,
            "expected_urgency": item.get("expected_urgency"),
            "routing_category_id": pipeline_output["routing_category_id"],
            "inferred_subcategory_id": pipeline_output["inferred_subcategory_id"],
            "likely_institution": pipeline_output["routing"]["likely_institution"],
            "sector": pipeline_output["routing"]["sector"],
            "urgency": pipeline_output["routing"].get("urgency", pipeline_output["routing"].get("urgency_default")),
            "human_review_required": pipeline_output["routing"]["human_review_required"],
            "routing_level": pipeline_output["routing"]["routing_level"]
        }

        results.append(result_row)

    if total - unknown_expected > 0:
        accuracy = correct_category / (total - unknown_expected)
    else:
        accuracy = 0

    with open(OUTPUT_PATH, "w", encoding="utf-8") as output_file:
        for row in results:
            output_file.write(json.dumps(row, ensure_ascii=False) + "\n")

    print("=" * 80)
    print("Darija Dataset Evaluation")
    print("=" * 80)
    print(f"Total examples: {total}")
    print(f"Examples with expected category: {total - unknown_expected}")
    print(f"Correct category predictions: {correct_category}")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Results saved to: {OUTPUT_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    evaluate()
