# Baseline Grievance Classifier v1
# Purpose: simple rule-based categorization and routing for Moroccan Darija/Arabic grievances

def classify_grievance(transcript):
    text = transcript.lower()

    categories = {
        "financial_crime": [
            "غسل الأموال", "تبييض الأموال", "حسابات بنكية", "تحويلات", "فواتير",
            "شركات", "عقارات", "أموال", "مليار", "مليون"
        ],
        "court_legal": [
            "محكمة", "جلسة", "متهم", "محامي", "الأستاذ", "قاضي",
            "حكم", "القانون الجنائي", "المنسوب إليك", "جنحة", "جناية"
        ],
        "civil_registry": [
            "عقد الازدياد", "الحالة المدنية", "البطاقة الوطنية", "كناش الحالة المدنية"
        ],
        "municipal_services": [
            "الجماعة", "المقاطعة", "الزبالة", "النفايات", "الإنارة", "الطريق"
        ],
        "land_property": [
            "العقار", "الأرض", "الملكية", "المحافظة العقارية", "رخصة البناء"
        ],
        "police_security": [
            "الشرطة", "الأمن", "الدرك", "محضر", "سرقة", "اعتداء", "تهديد"
        ],
        "health": [
            "مستشفى", "طبيب", "علاج", "حالة مستعجلة", "الصحة"
        ],
        "education": [
            "مدرسة", "جامعة", "أستاذ", "تلميذ", "تسجيل", "منحة"
        ],
        "utilities": [
            "الماء", "الكهرباء", "الضو", "فاتورة", "انقطاع"
        ],
        "labor_employment": [
            "خدمة", "عقد عمل", "أجرة", "مشغل", "ضمان اجتماعي", "CNSS"
        ],
        "general_administration": [
            "ملف", "طلب", "تأخر", "جواب", "إدارة", "وثيقة"
        ]
    }

    routing_map = {
        "financial_crime": "Justice institution / financial investigation authority",
        "court_legal": "Justice institution / court clerk",
        "civil_registry": "Commune civil registry office",
        "municipal_services": "Commune / municipality",
        "land_property": "Land registry / conservation foncière",
        "police_security": "Police / gendarmerie",
        "health": "Hospital administration / health authority",
        "education": "School or education authority",
        "utilities": "Utility provider",
        "labor_employment": "Labor inspectorate / employment authority",
        "general_administration": "Relevant public administration"
    }

    sensitive_categories = [
        "financial_crime",
        "court_legal",
        "police_security",
        "health",
        "land_property",
        "civil_registry",
        "labor_employment"
    ]

    matched_categories = []

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in text:
                matched_categories.append(category)
                break

    if not matched_categories:
        category = "unclear_needs_review"
        institution = "Human employee review"
        urgency = "medium"
        human_review = True
        confidence = 0.30
    else:
        priority_order = [
            "financial_crime",
            "court_legal",
            "police_security",
            "health",
            "land_property",
            "civil_registry",
            "labor_employment",
            "general_administration",
            "municipal_services",
            "utilities",
            "education"
        ]

        category = next((cat for cat in priority_order if cat in matched_categories), matched_categories[0])
        institution = routing_map.get(category, "Human employee review")
        human_review = category in sensitive_categories or len(matched_categories) > 1
        confidence = 0.75 if len(matched_categories) == 1 else 0.60

        if category in ["financial_crime", "court_legal", "police_security", "health"]:
            urgency = "high"
        elif category in ["general_administration", "civil_registry", "land_property", "labor_employment"]:
            urgency = "medium"
        else:
            urgency = "low"

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
