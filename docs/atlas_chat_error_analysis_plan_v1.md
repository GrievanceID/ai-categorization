# Atlas-Chat Error Analysis Plan v1

## Purpose

This document explains how we will evaluate Atlas-Chat for grievance categorization and routing.

Since Atlas-Chat is currently reported to have around 70% accuracy, the goal is not to fine-tune immediately. The goal is to understand why the remaining errors happen.

The results of this analysis will help us decide whether we need:

- better prompts,
- a stronger Moroccan legal/government lexicon,
- clearer category definitions,
- more labeled examples,
- or future fine-tuning.

---

## Current situation

The project already has a rule-based baseline classifier.

Baseline files include:

- `src/baseline_grievance_classifier.py`
- `data/rules/category_keyword_rules_v1.json`
- `data/taxonomy/category_taxonomy_v1.csv`
- `data/routing/routing_map_v1.csv`

Atlas-Chat will be tested as the smarter AI model for categorization and routing.

---

## Main research question

Can Atlas-Chat correctly classify Moroccan grievance transcripts using the official Chikaya.ma-style grievance categories?

---

## Step 1 — Collect Chikaya.ma categories

The first step is to collect the official grievance categories used by Chikaya.ma.

These categories should be saved in a clean file later, for example:

`data/taxonomy/chikaya_categories_v1.csv`

Each category should include:

- category name
- short definition
- example keywords
- possible institution or sector
- notes if the category is sensitive

---

## Step 2 — Align Chikaya.ma categories with our taxonomy

After collecting the Chikaya.ma categories, we compare them with our existing taxonomy:

`data/taxonomy/category_taxonomy_v1.csv`

The goal is to check:

- which categories already match,
- which categories need to be renamed,
- which categories are missing,
- which categories are too broad,
- which categories are too specific.

---

## Step 3 — Build an Atlas-Chat test set

Create test complaints for each Chikaya.ma category.

The test set should include different language styles:

- Darija
- Arabic / MSA
- French
- mixed Darija-Arabic-French
- unclear ASR-style transcript

Each test case should include:

- input transcript
- expected category
- expected institution or sector
- expected urgency
- expected human review flag

---

## Step 4 — Run Atlas-Chat

Atlas-Chat should receive:

1. the grievance transcript,
2. the list of allowed Chikaya.ma categories,
3. clear output instructions.

Atlas-Chat should return:

- grievance_category
- institution_category
- primary_institution
- urgency
- summary
- confidence_score
- human_review_flag
- reasoning_short

---

## Step 5 — Record results

For each test case, record:

- expected category
- Atlas-Chat predicted category
- whether the category was correct
- expected route
- Atlas-Chat predicted route
- whether the route was correct
- whether the summary was useful
- whether the human review flag was correct

---

## Step 6 — Analyze errors

For every wrong or partially correct result, identify the error type.

Possible error types:

- wrong category
- correct category but wrong institution
- confused two similar categories
- missed Darija keyword
- missed French administrative term
- misunderstood legal vocabulary
- failed on unclear ASR transcript
- missed urgency
- forgot human review flag
- summary invented information
- confidence score too high for uncertain case

---

## Step 7 — Decide improvement strategy

After error analysis, choose the correct improvement.

### If errors are mostly vocabulary errors

Improve:

- Moroccan Darija lexicon
- French administrative lexicon
- legal/government keyword rules
- prompt examples

Fine-tuning may not be needed yet.

### If errors are mostly category confusion

Improve:

- category definitions
- examples per category
- Chikaya.ma category descriptions
- prompt instructions

Fine-tuning may not be needed yet.

### If errors remain high after prompt and lexicon improvements

Then consider:

- fine-tuning,
- supervised classification,
- or creating a labeled Chikaya.ma-style grievance dataset.

---

## Evaluation table template

| Test ID | Transcript type | Expected category | Atlas-Chat category | Category result | Expected route | Atlas-Chat route | Route result | Error type | Notes |
|---|---|---|---|---|---|---|---|---|---|
| AC001 | Darija | Pending | Pending | Pending | Pending | Pending | Pending | Pending | Pending |
| AC002 | Arabic/MSA | Pending | Pending | Pending | Pending | Pending | Pending | Pending | Pending |
| AC003 | French | Pending | Pending | Pending | Pending | Pending | Pending | Pending | Pending |
| AC004 | Mixed | Pending | Pending | Pending | Pending | Pending | Pending | Pending | Pending |

---

## Success criteria

Atlas-Chat is useful if it can:

- classify most Chikaya.ma categories correctly,
- handle Darija, Arabic, and French,
- understand Moroccan administrative vocabulary,
- route complaints to the correct sector or institution,
- flag sensitive cases for human review,
- avoid inventing information in summaries.

---

## Current conclusion

Since Atlas-Chat is already reported to reach around 70% accuracy, we should not fine-tune immediately.

The next step is to analyze the remaining 30% errors.

If the mistakes are mostly caused by missing Moroccan legal, administrative, or Darija vocabulary, then we should first improve the lexicon and prompt.

If Atlas-Chat still struggles after that, then fine-tuning may be justified.
