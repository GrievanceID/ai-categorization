# Grievance Classification Test Results v1

## Purpose

This file records the first manual test of the grievance categorization and routing prompt.

The goal is to check whether the prompt can correctly identify:

- grievance category
- routing institution
- urgency
- summary
- human review flag

---

## Test Method

I tested the baseline prompt using selected Darija/Arabic grievance examples from:

- `tests/grievance_classification_test_inputs_v1.md`
- `data/labeled_examples/grievance_routing_examples_v1.csv`

Each input was compared against the expected category, route, and human review flag.

---

## Test 1 — Administrative delay

Input:

بغيت نشكي حيت الملف ديالي بقا ثلاثة شهور ومازال ما خرجش من الجماعة

Expected category:

general_administration

Expected route:

Relevant public administration / commune

Expected human review:

true

Result:

Pending manual model test.

Notes:

This should be classified as an administrative delay. Human review is needed because the document type is not specified.

---

## Test 2 — Financial crime / legal

Input:

أنا بريء من جنحة غسل الأموال وما عنديش علاقة بالحسابات البنكية اللي قالو عليها

Expected category:

financial_crime

Expected route:

Justice institution / financial investigation authority

Expected human review:

true

Result:

Pending manual model test.

Notes:

This is sensitive because it mentions money laundering and bank accounts.

---

## Test 3 — Municipal services

Input:

بغيت نشكي على الزبالة ما تزادتش من الزنقة ديالنا جوج سيمانات

Expected category:

municipal_services

Expected route:

Commune / municipality

Expected human review:

false

Result:

Pending manual model test.

Notes:

This is a clear local service issue and can be routed with higher confidence.

---

## Test 4 — Health

Input:

المستشفى ما بغاوش يستقبلو الوالدة وهي عندها حالة مستعجلة

Expected category:

health

Expected route:

Hospital administration / health authority

Expected human review:

true

Result:

Pending manual model test.

Notes:

This should be high urgency because it mentions an emergency medical situation.

---

## Initial Finding

The test set covers different routing cases, including administration, financial crime, municipal services, and health.

The next step is to run these inputs through the baseline classification prompt using the local model selected by the team, then update the result field with:

- correct
- partially correct
- incorrect

This will help us identify which categories are easy to classify and which ones need more examples or better rules.
