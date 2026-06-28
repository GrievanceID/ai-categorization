# Grievance Router v1
# Purpose: route a classified grievance category/subcategory to the correct institution

import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

CATEGORY_ROUTING_PATH = BASE_DIR / "data" / "routing" / "category_to_institution_mapping_v1.csv"
SUBCATEGORY_ROUTING_PATH = BASE_DIR / "data" / "routing" / "subcategory_to_institution_mapping_v1.csv"


def load_csv_as_dict(path):
    rows = []
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows


def route_by_subcategory(category_id, subcategory_id):
    subcategory_routes = load_csv_as_dict(SUBCATEGORY_ROUTING_PATH)

    for row in subcategory_routes:
        if row["category_id"] == category_id and row["subcategory_id"] == subcategory_id:
            return {
                "category_id": row["category_id"],
                "subcategory_id": row["subcategory_id"],
                "subcategory_ar": row["subcategory_ar"],
                "likely_institution": row["likely_institution"],
                "sector": row["sector"],
                "urgency": row["urgency"],
                "human_review_required": row["human_review_required"],
                "notes": row["notes"],
                "routing_level": "subcategory"
            }

    return None


def route_by_category(category_id):
    category_routes = load_csv_as_dict(CATEGORY_ROUTING_PATH)

    for row in category_routes:
        if row["category_id"] == category_id:
            return {
                "category_id": row["category_id"],
                "category_ar": row["category_ar"],
                "likely_institution": row["likely_institution"],
                "sector": row["sector"],
                "urgency_default": row["urgency_default"],
                "human_review_required": row["human_review_required"],
                "notes": row["notes"],
                "routing_level": "category"
            }

    return {
        "category_id": category_id,
        "likely_institution": "مراجعة بشرية",
        "sector": "غير محدد",
        "urgency_default": "متوسط",
        "human_review_required": "yes",
        "notes": "No routing match found. Human review required.",
        "routing_level": "fallback"
    }


def route_grievance(category_id, subcategory_id=None):
    if subcategory_id:
        subcategory_result = route_by_subcategory(category_id, subcategory_id)
        if subcategory_result:
            return subcategory_result

    return route_by_category(category_id)


if __name__ == "__main__":
    test_cases = [
        {
            "category_id": "services_municipaux",
            "subcategory_id": "dechets"
        },
        {
            "category_id": "sante",
            "subcategory_id": "urgence_negligee"
        },
        {
            "category_id": "justice",
            "subcategory_id": "detention_arbitraire"
        },
        {
            "category_id": "eau_electricite",
            "subcategory_id": "facture_abusive"
        },
        {
            "category_id": "etat_civil",
            "subcategory_id": "acte_naissance"
        },
        {
            "category_id": "autre",
            "subcategory_id": None
        }
    ]

    for case in test_cases:
        result = route_grievance(
            case["category_id"],
            case["subcategory_id"]
        )
        print(result)
