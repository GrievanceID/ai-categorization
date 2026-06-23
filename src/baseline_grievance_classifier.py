# Baseline Grievance Classifier v2
# Purpose: rule-based categorization and routing using external JSON keyword rules

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
RULES_PATH = BASE_DIR / "data" / "rules" / "category_keyword_rules_v1.json"


ROUTING_MAP = {
    "financial_crime": "Justice institution / financial investigation authority",
    "court_legal": "Justice institution / court clerk",
    "civil_registry": "Commune civil registry office",
    "municipal_services": "Commune / municipality",
    "land_property": "Land registry / conservation foncière",
    "police_security": "Police / gendarmerie",
    "health": "Hospital administration / health authority",
    "education": "School or education authority",
    "utilities": "Utility provider",
    "transport": "Transport authority",
    "tax_business": "Tax authority / commerce administration",
    "social_protection": "Social protection authority",
    "labor_employment": "Labor inspectorate / employment authority",
    "general_administration": "Relevant public administration",
    "unclear_needs_review": "Human employee review"
}


def load_rules():
    with open(RULES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def classify_grievance(transcript):
    rules = load_rules()
    text = transcript.lower()

    matched_categories = []

    for category, rule_data in rules.items():
        keywords = rule_data.get("keywords", [])

        for keyword in keywords:
            if keyword.lower() in text:
                matched_categories.append(category)
                break

    if not matched_categories:
        category = "unclear_needs_review"
        institution = ROUTING_MAP[category]
        urgency = "medium"
        human_review = True
        confidence = 0.30
    else:
        matched_categories = sorted(
            matched_categories,
            key=lambda cat: rules[cat].get("priority", 99)
        )

        category = matched_categories[0]
        institution = ROUTING_MAP.get(category, "Human employee review")
        urgency = rules[category].get("default_urgency", "medium")

        is_sensitive = rules[category].get("sensitive", False)
        multiple_matches = len(matched_categories) > 1

        human_review = is_sensitive or multiple_matches
        confidence = 0.75 if len(matched_categories) == 1 else 0.60

    return {
        "input_transcript": transcript,
        "grievance_category": category,
        "primary_institution": institution,
        "urgency": urgency,
        "summary": "Baseline summary: the transcript was classified based on keyword signals.",
        "confidence_score": confidence,
        "human_review_flag": human_review,
        "matched_categories": matched_categories
    }


if __name__ == "__main__":
    test_examples = [
        "بغيت نشكي حيت الملف ديالي بقا ثلاثة شهور ومازال ما خرجش من الجماعة",
        "أنا بريء من جنحة غسل الأموال وما عنديش علاقة بالحسابات البنكية",
        "المستشفى ما بغاوش يستقبلو الوالدة وهي عندها حالة مستعجلة",
        "بغيت نشكي على الزبالة ما تزادتش من الزنقة ديالنا جوج سيمانات"
    ]

    for example in test_examples:
        result = classify_grievance(example)
        print(result)
