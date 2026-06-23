# AI Categorization and Routing

## Categorization and Routing Layer

This repository contains the AI categorization and routing preparation for the voice-based citizen grievance platform.

The goal of this component is to take a corrected or speaker-labeled transcript and convert it into a structured grievance case.

## Input

Corrected transcript or diarized transcript.

## Output

The system should return:

- grievance category
- routing institution
- urgency level
- short summary
- confidence score
- human review flag

## Current files

- `data/taxonomy/category_taxonomy_v1.csv`  
  Defines the main grievance categories, such as court/legal, financial crime, civil registry, municipal services, health, education, utilities, and general administration.

- `data/routing/routing_map_v1.csv`  
  Maps each category to the likely institution or public-service body that should receive the case.

- `data/labeled_examples/grievance_routing_examples_v1.csv`  
  Contains labeled Darija/Arabic grievance examples with category, routing institution, urgency, summary, and human-review flag.

- `prompts/grievance_classification_prompt_v1.md`  
  Baseline prompt for testing whether an AI model can classify and route grievance transcripts.

- `tests/grievance_classification_test_inputs_v1.md`  
  Test examples used to evaluate whether the classification/routing prompt gives the expected output.

## Why this matters

The speech pipeline produces a transcript, but the government platform needs more than text. It needs to understand:

1. What the complaint is about.
2. Which institution should receive it.
3. Whether the case is urgent.
4. Whether automatic routing is safe.
5. Whether a human employee should review the case first.

This layer separates `grievance_category` from `institution_category`.

This is important because the model may correctly understand the content but choose the wrong destination. Keeping them separate allows an employee to correct routing without changing the underlying content classification.

## Human review safeguard

Cases are flagged for human review when:

- the transcript is unclear
- legal charges are mentioned
- financial amounts are mentioned
- identity documents are involved
- health or safety risk is possible
- multiple institutions may be relevant
- confidence is low

The system should not silently auto-route sensitive or uncertain cases.
