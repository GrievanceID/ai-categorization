# Baseline Classifier Evaluation v1

## Purpose

This file evaluates the rule-based baseline grievance classifier against selected test cases.

The goal is to check whether the classifier correctly predicts:

- grievance category
- routing institution
- urgency
- human review flag

---

## Evaluation method

Each test case is compared against the expected output.

A result can be:

- correct
- partially correct
- incorrect

---

## Test Case 1 — Administrative delay

Input:

بغيت نشكي حيت الملف ديالي بقا ثلاثة شهور ومازال ما خرجش من الجماعة

Expected category:

general_administration

Classifier category:

general_administration

Result:

correct

Notes:

The classifier detected the administrative delay through words such as ملف and الجماعة. Human review is appropriate because more than one category can be relevant.

---

## Test Case 2 — Financial crime / legal complaint

Input:

أنا بريء من جنحة غسل الأموال وما عنديش علاقة بالحسابات البنكية

Expected category:

financial_crime

Classifier category:

financial_crime

Result:

correct

Notes:

The classifier correctly prioritized financial_crime because the transcript includes غسل الأموال and حسابات بنكية.

---

## Test Case 3 — Health emergency

Input:

المستشفى ما بغاوش يستقبلو الوالدة وهي عندها حالة مستعجلة

Expected category:

health

Classifier category:

health

Result:

correct

Notes:

The classifier correctly detected a health issue and assigned high urgency because the transcript mentions مستشفى and حالة مستعجلة.

---

## Test Case 4 — Municipal garbage complaint

Input:

بغيت نشكي على الزبالة ما تزادتش من الزنقة ديالنا جوج سيمانات

Expected category:

municipal_services

Classifier category:

municipal_services

Result:

correct

Notes:

The classifier correctly detected a municipal service issue through the word الزبالة.

---

## Initial evaluation summary

Total test cases:

4

Correct:

4

Partially correct:

0

Incorrect:

0

Initial accuracy:

100% on the four sample test cases.

---

## Important limitation

This result only shows that the baseline works on four simple examples.

It does not mean the classifier is fully accurate for real citizen grievances.

More examples are needed, especially for:

- mixed Darija/French complaints
- unclear ASR transcripts
- multi-category complaints
- legal and court-related speech
- administrative complaints without obvious keywords

---

## Next step

The next step is to expand the test set and compare this rule-based baseline with an AI model such as Atlas-Chat, DarijaBERT, or AraBERT.
