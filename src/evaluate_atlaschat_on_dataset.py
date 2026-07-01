# Evaluate AtlasChat on Darija Dataset
# Purpose: run AtlasChat through Ollama and calculate category accuracy

import json
import argparse
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "data" / "test_datasets" / "test_dataset_darija.jsonl"
OUTPUT_PATH = BASE_DIR / "tests" / "transformer_results" / "atlaschat_results.jsonl"
SUMMARY_PATH = BASE_DIR / "tests" / "transformer_results" / "atlaschat_summary.txt"


ALLOWED_CATEGORIES = [
    "administration_generale",
    "sante",
    "education",
    "services_municipaux",
    "eau_electricite",
    "logement_urbanisme",
    "foncier_cadastre",
    "justice",
    "police_securite",
    "fiscal_financier",
    "emploi",
    "transport",
    "etat_civil",
    "environnement",
    "telecoms_numerique",
    "autre"
]


def load_jsonl(path):
    rows = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))

    return rows


def get_text(row):
    return row.get("text") or row.get("transcript") or row.get("complaint")


def get_expected_category(row):
    return row.get("expected_category") or row.get("category") or row.get("label")


def build_prompt(text):
    categories_text = "\n".join(f"- {cat}" for cat in ALLOWED_CATEGORIES)

    return f"""
You are an AI classifier for Moroccan citizen grievances.

Classify the complaint into exactly ONE category from the allowed list.

Allowed categories:
{categories_text}

Complaint:
{text}

Return ONLY valid JSON.
Do not write any explanation before or after the JSON.
Do not use markdown.
Do not use Arabic field names.
Use exactly this format:

{{
  "predicted_category": "one_category_id_from_allowed_list",
  "confidence": 0.0,
  "reasoning_short": "short reason"
}}
"""


def run_ollama(model_name, prompt):
    result = subprocess.run(
        ["ollama", "run", model_name],
        input=prompt,
        text=True,
        capture_output=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result.stdout.strip()


def extract_json(text):
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    # Fallback: if AtlasChat did not return valid JSON,
    # search for any allowed category name inside the raw output.
    for category in ALLOWED_CATEGORIES:
        if category in text:
            return {
                "predicted_category": category,
                "confidence": 0.0,
                "reasoning_short": "Recovered from non-JSON output"
            }

    return None


def evaluate(model_name, limit=None):
    dataset = load_jsonl(DATASET_PATH)

    if limit:
        dataset = dataset[:limit]

    total = 0
    correct = 0
    failed_parse = 0
    results = []

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    for index, row in enumerate(dataset, start=1):
        text = get_text(row)
        expected = get_expected_category(row)

        if not text or not expected:
            continue

        print(f"Testing {index}/{len(dataset)}...")

        prompt = build_prompt(text)
        raw_output = run_ollama(model_name, prompt)
        parsed = extract_json(raw_output)

        if parsed is None:
            predicted = None
            failed_parse += 1
        else:
            predicted = parsed.get("predicted_category")

        is_correct = predicted == expected

        total += 1
        if is_correct:
            correct += 1

        result_row = {
            "id": row.get("id", index),
            "text": text,
            "expected_category": expected,
            "atlaschat_predicted_category": predicted,
            "correct": is_correct,
            "raw_output": raw_output
        }

        results.append(result_row)

        with open(OUTPUT_PATH, "w", encoding="utf-8") as output_file:
            for item in results:
                output_file.write(json.dumps(item, ensure_ascii=False) + "\n")

    accuracy = correct / total if total else 0

    summary = (
        "AtlasChat Evaluation\n"
        f"Model: {model_name}\n"
        f"Total tested: {total}\n"
        f"Correct: {correct}\n"
        f"Accuracy: {accuracy:.2%}\n"
        f"Failed JSON parse: {failed_parse}\n"
        f"Results file: {OUTPUT_PATH}\n"
    )

    with open(SUMMARY_PATH, "w", encoding="utf-8") as file:
        file.write(summary)

    print("=" * 80)
    print(summary)
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model_name",
        type=str,
        required=True,
        help="Exact Ollama model name"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional number of examples to test first"
    )

    args = parser.parse_args()

    evaluate(args.model_name, args.limit)
