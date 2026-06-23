# Categorization and Routing Progress Summary v1

## Contributor

Mira / Amira

## Component

AI Categorization and Routing Layer

## Purpose

This component takes a corrected or speaker-labeled grievance transcript and converts it into a structured case.

The structured case includes:

- grievance category
- routing institution
- urgency level
- short summary
- confidence score
- human review flag

---

## Work completed

### 1. Category taxonomy

Created:

`data/taxonomy/category_taxonomy_v1.csv`

This file defines the main grievance categories, including:

- court/legal
- financial crime
- civil registry
- municipal services
- land/property
- police/security
- health
- education
- utilities
- transport
- tax/business
- social protection
- labor/employment
- general administration
- unclear/needs review

---

### 2. Routing map

Created:

`data/routing/routing_map_v1.csv`

This file maps each grievance category to the likely institution or public-service body.

Example:

- financial_crime → Justice institution / financial investigation authority
- municipal_services → Commune / municipality
- health → Hospital administration / health authority
- utilities → Utility provider

---

### 3. Labeled examples

Created:

`data/labeled_examples/grievance_routing_examples_v1.csv`

This file contains Darija/Arabic grievance examples with expected category, route, urgency, summary, and human-review flag.

---

### 4. Classification prompt

Created:

`prompts/grievance_classification_prompt_v1.md`

This prompt is used to test whether an AI model can classify and route grievance transcripts.

---

### 5. Test inputs and test results

Created:

`tests/grievance_classification_test_inputs_v1.md`

`tests/grievance_classification_test_results_v1.md`

These files define sample test cases and record the expected behavior of the categorization/routing layer.

---

### 6. Output schema

Created:

`schemas/grievance_case_output_schema_v1.json`

This file defines the structured output format for a grievance case.

---

### 7. Baseline classifier

Created:

`src/baseline_grievance_classifier.py`

This is a simple rule-based Python baseline classifier.

It uses keyword matching to:

- detect grievance category
- map the category to an institution
- estimate urgency
- decide if human review is needed

---

### 8. Local test

Created:

`tests/local_baseline_script_test_v1.md`

The baseline script was tested locally using Python 3.

The script successfully classified four sample grievances:

- administrative delay
- financial crime/legal complaint
- health emergency
- municipal garbage complaint

---

### 9. Sample outputs

Created:

`examples/sample_baseline_outputs_v1.md`

This file shows example input transcripts and the structured outputs produced by the baseline classifier.

---

## Current status

The first version of the categorization and routing layer is complete as a baseline.

It is not the final AI model yet, but it provides a working foundation for testing and improving the system.

---

## Next steps

The next technical steps are:

1. improve the keyword rules using more examples,
2. compare baseline outputs against Atlas-Chat or another local model,
3. add more Darija/Arabic/French grievance examples,
4. evaluate which categories are easy or difficult to classify,
5. prepare for a future supervised or fine-tuned model.
