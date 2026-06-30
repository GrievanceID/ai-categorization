# Train Transformer Classifier
# Purpose: fine-tune AraBERT or DarijaBERT on grievance category classification

import json
import argparse
from pathlib import Path

import numpy as np
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
from sklearn.metrics import accuracy_score, f1_score, classification_report


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "prepared_transformer_dataset"

TRAIN_PATH = DATA_DIR / "train.jsonl"
TEST_PATH = DATA_DIR / "test.jsonl"
LABEL_MAP_PATH = DATA_DIR / "label_map.json"

RESULTS_DIR = BASE_DIR / "tests" / "transformer_results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_jsonl(path):
    rows = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))

    return rows


def load_label_map():
    with open(LABEL_MAP_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def compute_metrics(pred):
    labels = pred.label_ids
    predictions = np.argmax(pred.predictions, axis=1)

    return {
        "accuracy": accuracy_score(labels, predictions),
        "macro_f1": f1_score(labels, predictions, average="macro")
    }


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model_name",
        type=str,
        required=True,
        help="Hugging Face model name, e.g. aubmindlab/bert-base-arabertv02"
    )

    parser.add_argument(
        "--output_name",
        type=str,
        required=True,
        help="Short output name, e.g. arabert or darijabert"
    )

    args = parser.parse_args()

    label_map = load_label_map()
    num_labels = label_map["num_labels"]
    id_to_label = {int(k): v for k, v in label_map["id_to_label"].items()}
    label_to_id = label_map["label_to_id"]

    train_rows = load_jsonl(TRAIN_PATH)
    test_rows = load_jsonl(TEST_PATH)

    train_dataset = Dataset.from_list(train_rows)
    test_dataset = Dataset.from_list(test_rows)

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    def tokenize(batch):
        return tokenizer(
            batch["text"],
            padding="max_length",
            truncation=True,
            max_length=128
        )

    train_dataset = train_dataset.map(tokenize, batched=True)
    test_dataset = test_dataset.map(tokenize, batched=True)

    train_dataset = train_dataset.rename_column("label_id", "labels")
    test_dataset = test_dataset.rename_column("label_id", "labels")

    columns_to_keep = ["input_ids", "attention_mask", "labels"]

    train_dataset = train_dataset.remove_columns(
        [col for col in train_dataset.column_names if col not in columns_to_keep]
    )

    test_dataset = test_dataset.remove_columns(
        [col for col in test_dataset.column_names if col not in columns_to_keep]
    )

    train_dataset.set_format("torch")
    test_dataset.set_format("torch")

    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name,
        num_labels=num_labels,
        id2label=id_to_label,
        label2id=label_to_id
    )

    training_args = TrainingArguments(
        output_dir=str(RESULTS_DIR / args.output_name),
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_steps=5,
        load_best_model_at_end=True
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics
    )

    trainer.train()

    predictions = trainer.predict(test_dataset)
    predicted_labels = np.argmax(predictions.predictions, axis=1)
    true_labels = predictions.label_ids

    target_names = [id_to_label[i] for i in range(num_labels)]

    report = classification_report(
        true_labels,
        predicted_labels,
        target_names=target_names,
        zero_division=0
    )

    metrics = compute_metrics(predictions)

    results_path = RESULTS_DIR / f"{args.output_name}_results.txt"

    with open(results_path, "w", encoding="utf-8") as file:
        file.write(f"Model: {args.model_name}\n")
        file.write(f"Accuracy: {metrics['accuracy']}\n")
        file.write(f"Macro F1: {metrics['macro_f1']}\n\n")
        file.write(report)

    print("=" * 80)
    print(f"Model tested: {args.model_name}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Macro F1: {metrics['macro_f1']:.4f}")
    print(f"Results saved to: {results_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
