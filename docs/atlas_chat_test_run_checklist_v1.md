# Atlas-Chat Test Run Checklist v1

## Purpose

This checklist explains how to run Atlas-Chat tests for Chikaya-style categorization and routing.

The goal is to make sure every test is done in the same way.

---

## Before testing

Make sure these files are ready:

- `prompts/atlas_chat_chikaya_routing_prompt_v1.md`
- `tests/chikaya_routing_alignment_test_cases_v1.md`
- `tests/atlas_chat_chikaya_routing_results_v1.md`
- `data/routing/chikaya_routing_alignment_v1.csv`

---

## Test steps

### Step 1 — Open the prompt

Open:

`prompts/atlas_chat_chikaya_routing_prompt_v1.md`

Copy the full prompt.

---

### Step 2 — Choose one test case

Open:

`tests/chikaya_routing_alignment_test_cases_v1.md`

Choose one transcript.

Example:

المستشفى ما بغاوش يستقبلو الوالدة وهي عندها حالة مستعجلة

---

### Step 3 — Paste into Atlas-Chat

Paste the prompt into Atlas-Chat.

Then replace:

`[PASTE TRANSCRIPT HERE]`

with the selected transcript.

---

### Step 4 — Save the output

Copy Atlas-Chat’s output.

Record the result in:

`tests/atlas_chat_chikaya_routing_results_v1.md`

---

### Step 5 — Compare with expected answer

Check:

- expected category
- Atlas-Chat category
- expected Chikaya sector
- Atlas-Chat sector
- human review flag
- summary quality
- confidence score

---

### Step 6 — Mark result

Use one of these labels:

- correct
- partially correct
- incorrect

---

### Step 7 — Add error type

If the result is wrong, choose an error type:

- wrong_category
- wrong_sector
- correct_category_wrong_sector
- missed_darija_keyword
- missed_french_term
- confused_similar_categories
- missed_human_review
- low_confidence_needed
- invented_summary
- unclear_output_format

---

## Important testing rules

Do not change the prompt between test cases.

Use the same category list every time.

Do not give Atlas-Chat the expected answer.

Do not correct Atlas-Chat during the test.

Record the first output, even if it is wrong.

---

## Why this matters

If every test is run in the same way, the results will be fair.

This helps us decide whether Atlas-Chat needs:

- better prompt instructions,
- more examples,
- stronger lexicon,
- clearer Chikaya category mapping,
- or future fine-tuning.
