# Local Baseline Script Test v1

## Purpose

This file records the first local test of the baseline grievance classifier script.

## Script tested

`src/baseline_grievance_classifier.py`

## Command used

python3 src/baseline_grievance_classifier.py

## Test status

Completed successfully.

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

The script ran successfully using Python 3.

This confirms that the first rule-based baseline can categorize a transcript, map it to an institution, estimate urgency, and decide whether human review is needed.

This is not the final AI model, but it provides a working baseline before testing larger models such as Atlas-Chat, DarijaBERT, or AraBERT.
