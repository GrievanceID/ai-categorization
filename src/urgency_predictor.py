# Urgency Predictor v1
# Purpose: combine category default urgency with urgency keyword rules

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

CATEGORIES_PATH = BASE_DIR / "data" / "taxonomy" / "categories_ar.json"
URGENCY_RULES_PATH = BASE_DIR / "data" / "rules" / "urgency_keyword_rules_v1.json"


URGENCY_PRIORITY = {
    "منخفض": 1,
    "متوسط": 2,
    "عالي": 3
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_category_default_urgency(category_id):
    data = load_json(CATEGORIES_PATH)

    for category in data["categories"]:
        if category["id"] == category_id:
            return category["default_urgency"]

    return "متوسط"


def detect_keyword_urgency(text):
    rules = load_json(URGENCY_RULES_PATH)

    matched_keywords = []
    detected_urgencies = []

    for urgency_key, urgency_data in rules.items():
        label_ar = urgency_data["label_ar"]

        for keyword in urgency_data["keywords"]:
            if keyword.lower() in text.lower():
                matched_keywords.append({
                    "keyword": keyword,
                    "urgency": label_ar
                })
                detected_urgencies.append(label_ar)

    if not detected_urgencies:
        return None, matched_keywords

    highest_urgency = max(
        detected_urgencies,
        key=lambda urgency: URGENCY_PRIORITY.get(urgency, 0)
    )

    return highest_urgency, matched_keywords


def predict_urgency(text, category_id):
    default_urgency = get_category_default_urgency(category_id)
    keyword_urgency, matched_keywords = detect_keyword_urgency(text)

    if keyword_urgency is None:
        final_urgency = default_urgency
        decision_source = "category_default"
    else:
        if URGENCY_PRIORITY[keyword_urgency] > URGENCY_PRIORITY[default_urgency]:
            final_urgency = keyword_urgency
            decision_source = "keyword_override"
        else:
            final_urgency = default_urgency
            decision_source = "category_default"

    return {
        "category_id": category_id,
        "default_urgency": default_urgency,
        "keyword_urgency": keyword_urgency,
        "final_urgency": final_urgency,
        "matched_keywords": matched_keywords,
        "decision_source": decision_source
    }


if __name__ == "__main__":
    test_cases = [
        {
            "text": "المستشفى ما بغاوش يستقبلو الوالدة وهي عندها حالة مستعجلة",
            "category_id": "sante"
        },
        {
            "text": "بغيت نشكي على الزبالة ما تزادتش من الزنقة ديالنا",
            "category_id": "services_municipaux"
        },
        {
            "text": "الملف ديالي تأخر ثلاثة شهور وما جاوبونيش",
            "category_id": "administration_generale"
        },
        {
            "text": "الماء مقطوع علينا من ثلاثة أيام",
            "category_id": "eau_electricite"
        }
    ]

    for case in test_cases:
        result = predict_urgency(case["text"], case["category_id"])
        print(result)
