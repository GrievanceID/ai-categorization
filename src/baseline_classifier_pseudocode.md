# Baseline Classifier Pseudocode v1

## Purpose

This document describes the first simple logic for the categorization and routing layer.

The goal is to take a transcript and produce a structured grievance case with:

- grievance category
- routing institution
- urgency
- summary
- confidence score
- human review flag

---

## Input

A corrected or diarized transcript.

Example:

بغيت نشكي حيت الملف ديالي بقا ثلاثة شهور ومازال ما خرجش من الجماعة

---

## Output

A structured case following:

`schemas/grievance_case_output_schema_v1.json`

---

## Baseline Logic

### Step 1 — Load support files

Load:

- `data/taxonomy/category_taxonomy_v1.csv`
- `data/routing/routing_map_v1.csv`
- `data/lexicon/government_legal_lexicon_seed.csv`
- `schemas/grievance_case_output_schema_v1.json`

---

### Step 2 — Normalize transcript

Clean the transcript by:

- removing extra spaces
- normalizing repeated spellings
- correcting known ASR mistakes using the lexicon
- keeping important Darija, Arabic, and French legal terms

Example:

غسي الأموال → غسل الأموال

---

### Step 3 — Detect category keywords

Check the transcript for strong category signals.

Examples:

- غسل الأموال, حسابات بنكية, تحويلات → financial_crime
- محكمة, جلسة, متهم, محامي → court_legal
- عقد الازدياد, الحالة المدنية → civil_registry
- الجماعة, الزبالة, الإنارة → municipal_services
- الماء, الكهرباء, الفاتورة → utilities
- مستشفى, طبيب, حالة مستعجلة → health

---

### Step 4 — Select grievance category

If one strong category is found, assign it.

If multiple categories are found, choose the most sensitive category first.

Priority order for sensitive cases:

1. financial_crime
2. court_legal
3. police_security
4. health
5. land_property
6. civil_registry
7. labor_employment
8. general_administration
9. municipal_services
10. utilities

If no category is clear, assign:

unclear_needs_review

---

### Step 5 — Map to routing institution

Use:

`data/routing/routing_map_v1.csv`

to map the selected category to the likely institution.

Example:

financial_crime → Justice institution / financial investigation authority

municipal_services → Commune / municipality

health → Hospital administration / health authority

---

### Step 6 — Estimate urgency

Use high urgency when the transcript includes:

- legal charge
- financial crime
- medical emergency
- police/security issue
- large financial amount
- serious harm or risk

Use medium urgency when:

- the issue is delayed
- documents are blocked
- an institution did not respond
- the issue affects access to public service

Use low urgency when:

- the issue is informational
- no harm or risk is mentioned
- the complaint is simple and clear

---

### Step 7 — Set human review flag

Set human_review_flag to true when:

- transcript is unclear
- category is uncertain
- more than one institution may be relevant
- legal charges are mentioned
- financial amounts are mentioned
- identity documents are involved
- health or safety risk is possible
- confidence is low

Otherwise, set it to false.

---

### Step 8 — Generate summary

Create a short factual summary.

The summary must not invent details.

Example:

Input:

بغيت نشكي حيت الملف ديالي بقا ثلاثة شهور ومازال ما خرجش من الجماعة

Summary:

Citizen complains that their file has been delayed for three months at the commune.

---

## Example Output

case_id: TEST_001  
grievance_category: general_administration  
institution_category: Relevant public administration / commune  
urgency: medium  
summary: Citizen complains that their file has been delayed for three months at the commune.  
confidence_score: 0.78  
human_review_flag: true  
reasoning_short: The issue is an administrative delay, but the document type is not specified.

---

## Next Step

Convert this pseudocode into a small Python script that can:

1. read a transcript,
2. check keywords,
3. assign a category,
4. map it to an institution,
5. return a structured case.
