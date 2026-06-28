# Grievance Categorization + Routing Pipeline v1
# Purpose: connect classification output to routing output

from baseline_grievance_classifier import classify_grievance
from grievance_router import route_grievance


CATEGORY_ID_MAP = {
    "general_administration": "administration_generale",
    "health": "sante",
    "education": "education",
    "municipal_services": "services_municipaux",
    "utilities": "eau_electricite",
    "land_property": "logement_urbanisme",
    "court_legal": "justice",
    "financial_crime": "fiscal_financier",
    "police_security": "police_securite",
    "labor_employment": "emploi",
    "transport": "transport",
    "civil_registry": "etat_civil",
    "tax_business": "fiscal_financier",
    "social_protection": "emploi",
    "unclear_needs_review": "autre"
}


SUBCATEGORY_HINTS = {
    "municipal_services": {
        "الزبالة": "dechets",
        "النفايات": "dechets",
        "الإنارة": "eclairage",
        "الطريق": "voirie",
        "الزنقة": "voirie"
    },
    "health": {
        "حالة مستعجلة": "urgence_negligee",
        "مستعجلة": "urgence_negligee",
        "دواء": "medicaments",
        "الأدوية": "medicaments",
        "استقبال": "mauvaise_prise_en_charge"
    },
    "utilities": {
        "الماء": "coupure_eau",
        "الكهرباء": "coupure_electricite",
        "فاتورة": "facture_abusive",
        "الربط": "raccordement"
    },
    "civil_registry": {
        "عقد الازدياد": "acte_naissance",
        "الحالة المدنية": "acte_naissance",
        "البطاقة الوطنية": "cin_passeport",
        "جواز السفر": "cin_passeport"
    },
    "labor_employment": {
        "الأجرة": "salaire_non_verse",
        "راتب": "salaire_non_verse",
        "CNSS": "cnss_non_declare",
        "فصل": "licenciement_abusif"
    }
}


def infer_subcategory(transcript, predicted_category):
    hints = SUBCATEGORY_HINTS.get(predicted_category, {})

    for keyword, subcategory_id in hints.items():
        if keyword.lower() in transcript.lower():
            return subcategory_id

    return None


def process_grievance(transcript):
    classification = classify_grievance(transcript)

    predicted_category = classification["grievance_category"]
    routing_category_id = CATEGORY_ID_MAP.get(predicted_category, "autre")

    subcategory_id = infer_subcategory(transcript, predicted_category)

    routing = route_grievance(routing_category_id, subcategory_id)

    return {
        "input_transcript": transcript,
        "classification": classification,
        "routing_category_id": routing_category_id,
        "inferred_subcategory_id": subcategory_id,
        "routing": routing
    }


if __name__ == "__main__":
    test_transcripts = [
        "بغيت نشكي على الزبالة ما تزادتش من الزنقة ديالنا جوج سيمانات",
        "المستشفى ما بغاوش يستقبلو الوالدة وهي عندها حالة مستعجلة",
        "الماء تقطع علينا ثلاثة أيام والفاتورة باقية طالعة",
        "مشيت نخرج عقد الازدياد ولكن مكتب الحالة المدنية قالو ليا الملف باقي ما وجدش",
        "المشغل ما عطانيش الأجرة ديالي وما صرحش بيا ف CNSS"
    ]

    for transcript in test_transcripts:
        result = process_grievance(transcript)
        print(result)
        print("-" * 80)
