# Categorization and Routing Checklist v1

## Completed

- [x] Created grievance category taxonomy
- [x] Created routing map from categories to institutions
- [x] Created labeled Darija/Arabic grievance examples
- [x] Created baseline classification prompt
- [x] Created test inputs
- [x] Created initial test results file
- [x] Created output schema
- [x] Created baseline classifier pseudocode
- [x] Created working baseline Python classifier
- [x] Added requirements file
- [x] Tested the Python classifier locally
- [x] Documented local test results
- [x] Added sample baseline outputs
- [x] Added progress summary

## Current baseline capabilities

The current baseline can:

- read a grievance transcript
- detect keyword signals
- assign a grievance category
- map the category to a likely institution
- estimate urgency
- decide whether human review is needed
- return a structured result

## Limitations

The current baseline is rule-based.

It cannot fully understand complex language yet. It may struggle with:

- unclear transcripts
- spelling variation in Darija
- mixed Arabic/French/Darija
- complaints involving multiple institutions
- cases where the keywords are not obvious
- legal meaning that needs deeper context

## Future improvements

- [ ] Add more labeled examples
- [ ] Improve Darija keyword coverage
- [ ] Add French administrative keywords
- [ ] Compare baseline against Atlas-Chat
- [ ] Compare baseline against DarijaBERT or AraBERT
- [ ] Add evaluation metrics
- [ ] Add confusion/error analysis
- [ ] Prepare for future fine-tuning if enough data is collected

## Final status

The categorization and routing component has a complete first baseline.

It is ready for testing, review, and future model comparison.
