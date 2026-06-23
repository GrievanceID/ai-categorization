# Sample Baseline Classifier Outputs v1

## Purpose

This file shows example outputs from the first rule-based grievance classifier.

The goal is to demonstrate how a grievance transcript becomes a structured case.

---

## Example 1 — Administrative delay

Input:

بغيت نشكي حيت الملف ديالي بقا ثلاثة شهور ومازال ما خرجش من الجماعة

Output:

- grievance_category: general_administration
- primary_institution: Relevant public administration
- urgency: medium
- confidence_score: 0.60
- human_review_flag: true
- matched_categories: municipal_services, general_administration

Notes:

The transcript mentions both a file delay and the commune. Because more than one category matched, human review is required.

---

## Example 2 — Financial crime / legal complaint

Input:

أنا بريء من جنحة غسل الأموال وما عنديش علاقة بالحسابات البنكية

Output:

- grievance_category: financial_crime
- primary_institution: Justice institution / financial investigation authority
- urgency: high
- confidence_score: 0.60
- human_review_flag: true
- matched_categories: financial_crime, court_legal

Notes:

The transcript mentions money laundering, bank accounts, and a legal charge. This is sensitive, so it must be reviewed by a human.

---

## Example 3 — Health emergency

Input:

المستشفى ما بغاوش يستقبلو الوالدة وهي عندها حالة مستعجلة

Output:

- grievance_category: health
- primary_institution: Hospital administration / health authority
- urgency: high
- confidence_score: 0.75
- human_review_flag: true
- matched_categories: health

Notes:

The transcript mentions a hospital and emergency situation, so the urgency is high.

---

## Example 4 — Municipal garbage complaint

Input:

بغيت نشكي على الزبالة ما تزادتش من الزنقة ديالنا جوج سيمانات

Output:

- grievance_category: municipal_services
- primary_institution: Commune / municipality
- urgency: low
- confidence_score: 0.75
- human_review_flag: false
- matched_categories: municipal_services

Notes:

This is a clear local service complaint. Since it is not sensitive and only one category matched, human review is not required.
