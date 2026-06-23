# Local Baseline Script Test v2

## Purpose

This file records the local test of the updated baseline grievance classifier.

## Script tested

`src/baseline_grievance_classifier.py`

## Rules file used

`data/rules/category_keyword_rules_v1.json`

## Command used

python3 src/baseline_grievance_classifier.py

## Test status

Completed successfully.

## What changed from v1

In v1, the keyword rules were written directly inside the Python script.

In v2, the classifier loads the category keyword rules from an external JSON file:

`data/rules/category_keyword_rules_v1.json`

This makes the system easier to update because new keywords can be added without changing the main classifier logic.

## Results observed

The script successfully classified four sample grievance transcripts:

1. Administrative delay  
   - category: general_administration
   - urgency: medium
   - human_review_flag: true

2. Financial crime / legal complaint  
   - category: financial_crime
   - urgency: high
   - human_review_flag: true

3. Health emergency complaint  
   - category: health
   - urgency: high
   - human_review_flag: true

4. Municipal garbage complaint  
   - category: municipal_services
   - urgency: low
   - human_review_flag: false

## Notes

The updated classifier ran successfully after pulling the latest repository changes.

The categorization and routing layer is now cleaner because:

- taxonomy defines the categories,
- routing map defines the institution destination,
- keyword rules define how categories are detected,
- Python script applies the classification logic.

This is still a rule-based baseline, but it is now easier to improve and compare against future AI models.
