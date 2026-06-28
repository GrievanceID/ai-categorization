# Atlas-Chat Chikaya Routing Results v1

## Purpose

This file records Atlas-Chat results for Chikaya-style grievance categorization and routing.

The goal is to evaluate whether Atlas-Chat can correctly classify Moroccan grievance transcripts and route them to the correct Chikaya-style sector.

---

## Prompt used

`prompts/atlas_chat_chikaya_routing_prompt_v1.md`

---

## Test cases used

`tests/chikaya_routing_alignment_test_cases_v1.md`

---

## Results table

| Test ID | Transcript type | Expected category | Atlas-Chat category | Category result | Expected Chikaya sector | Atlas-Chat sector | Sector result | Human review correct? | Error type | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| AC001 | Darija | health | Pending | Pending | الصحة | Pending | Pending | Pending | Pending | Hospital emergency case |
| AC002 | Darija | municipal_services | Pending | Pending | الجماعات الترابية | Pending | Pending | Pending | Pending | Garbage collection case |
| AC003 | Darija/Arabic | civil_registry | Pending | Pending | الداخلية | Pending | Pending | Pending | Pending | Birth certificate / civil registry case |
| AC004 | Arabic | financial_crime | Pending | Pending | العدل | Pending | Pending | Pending | Pending | Money laundering / bank accounts case |
| AC005 | Darija | land_property | Pending | Pending | الاسكان والتعمير | Pending | Pending | Pending | Pending | Building permit / land registry case |
| AC006 | Darija | utilities | Pending | Pending | البيئة والطاقة والمعادن | Pending | Pending | Pending | Pending | Water outage and bill case |
| AC007 | Darija/French | labor_employment | Pending | Pending | التشغيل والتقاعد والتأمين الاجتماعي | Pending | Pending | Pending | Pending | Salary and CNSS case |
| AC008 | Darija | unclear_needs_review | Pending | Pending | غير محدد | Pending | Pending | Pending | Pending | Unclear transcript case |

---

## Error type options

Use one of these labels when Atlas-Chat makes a mistake:

- correct
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

## How to fill this file

For each test case:

1. Copy the transcript from `tests/chikaya_routing_alignment_test_cases_v1.md`.
2. Run it using `prompts/atlas_chat_chikaya_routing_prompt_v1.md`.
3. Paste the Atlas-Chat category and sector into the table.
4. Mark whether the result is correct, partially correct, or incorrect.
5. Add the error type if needed.

---

## Initial status

Pending Atlas-Chat testing.

---

## Evaluation goal

The goal is to identify whether Atlas-Chat errors are mostly caused by:

- missing Darija vocabulary,
- unclear category definitions,
- confusing similar Chikaya sectors,
- weak routing logic,
- or the need for fine-tuning.

If most errors are vocabulary or prompt-related, we should improve the prompt and lexicon first.

If errors remain high after prompt and lexicon improvements, then fine-tuning may be justified.
