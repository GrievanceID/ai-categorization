# Category Urgency Loader
# Purpose: load default urgency values from categories_ar.json

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CATEGORIES_PATH = BASE_DIR / "data" / "taxonomy" / "categories_ar.json"


def load_categories():
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def build_category_urgency_dictionary():
    data = load_categories()

    urgency_dict = {}

    for category in data["categories"]:
        urgency_dict[category["id"]] = {
            "label_ar": category["label_ar"],
            "label_darija": category["label_darija"],
            "default_urgency": category["default_urgency"]
        }

    return urgency_dict


if __name__ == "__main__":
    urgency_dict = build_category_urgency_dictionary()

    for category_id, info in urgency_dict.items():
        print(category_id, "→", info["label_ar"], "→", info["default_urgency"])
