# Categorization and Routing Implementation Plan v1

## Purpose

This document explains how the AI categorization and routing layer will work after the speech-to-text and diarization pipeline produces a transcript.

The goal is to convert a corrected or speaker-labeled transcript into a structured grievance case that can be reviewed by an employee and routed to the correct public institution.

---

## Input

The input to this layer is a transcript from the ASR and diarization pipeline.

Possible input types:

- corrected transcript
- speaker-labeled transcript
- diarized transcript with timestamps

Example:

بغيت نشكي حيت الملف ديالي بقا ثلاثة شهور ومازال ما خرجش من الجماعة

---

## Output

The output should be a structured case containing:

- grievance category
- routing institution
- urgency level
- short summary
- confidence score
- human review flag
- short explanation for the decision

Example output fields:

- grievance_category: general_administration
- institution_category: Relevant public administration / commune
- urgency: medium
- summary: Citizen complains that their file has been delayed for three months at the commune.
- confidence_score: medium
- human_review_flag: true

---

## Pipeline

### Step 1 — Receive transcript

The system receives a corrected or speaker-labeled transcript from the previous pipeline stage.

If the transcript is speaker-labeled, the model should prioritize the citizen’s complaint and avoid confusing it with employee, judge, or lawyer speech.

---

### Step 2 — Normalize terms

The system checks the transcript against the legal/government lexicon.

This helps normalize repeated Darija, Arabic, and French administrative terms.

Examples:

- غسي الأموال → غسل الأموال
- الشكاية → شكاية
- المحضر → محضر
- الجماعة → commune / municipality
- المحافظة العقارية → land registry

---

### Step 3 — Classify content

The model predicts the main grievance category using the taxonomy file:

`data/taxonomy/category_taxonomy_v1.csv`

Examples:

- money laundering → financial_crime
- birth certificate → civil_registry
- water outage → utilities
- garbage collection → municipal_services
- hospital refusal → health

---

### Step 4 — Map category to institution

After classifying the content, the system uses the routing map:

`data/routing/routing_map_v1.csv`

This maps the category to a likely public institution.

Example:

- municipal_services → Commune / municipality
- health → Hospital administration / health authority
- land_property → Land registry / conservation foncière
- financial_crime → Justice institution / financial investigation authority

---

### Step 5 — Generate summary

The system creates a short summary of the case in clear language.

The summary should not add new information. It should only use facts found in the transcript.

---

### Step 6 — Estimate urgency

Urgency can be:

- low
- medium
- high

High urgency should be used when the transcript includes:

- health or safety risk
- legal charges
- financial crime
- police/security concern
- emergency language
- serious administrative harm

---

### Step 7 — Apply human review flag

The system should flag cases for human review when:

- the transcript is unclear
- the category is uncertain
- more than one institution may be relevant
- legal charges are mentioned
- financial amounts are mentioned
- identity documents are involved
- health or safety risk is possible
- confidence is low

Sensitive or uncertain cases should not be automatically routed.

---

## Important design decision

The system separates:

- grievance_category
- institution_category

This is important because the model may understand the content correctly but still choose the wrong destination.

An employee should be able to correct the routing destination without changing the original content classification.

---

## Current supporting files

- `data/taxonomy/category_taxonomy_v1.csv`
- `data/routing/routing_map_v1.csv`
- `data/labeled_examples/grievance_routing_examples_v1.csv`
- `prompts/grievance_classification_prompt_v1.md`
- `tests/grievance_classification_test_inputs_v1.md`
- `tests/grievance_classification_test_results_v1.md`

---

## Next technical step

The next step is to implement a small baseline classifier script that:

1. reads a transcript,
2. applies the classification prompt,
3. returns a structured case output,
4. compares the output against expected labels in the test file.

Later, if enough labeled examples are collected, the dataset can support fine-tuning or supervised classification.
