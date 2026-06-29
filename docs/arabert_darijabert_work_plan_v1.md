# AraBERT and DarijaBERT Work Plan v1

## Purpose

This document explains the plan for testing AraBERT and DarijaBERT on the Moroccan grievance categorization dataset.

The goal is to compare transformer-based category classification against:

- rule-based baseline
- AtlasChat
- AraBERT
- DarijaBERT

## Why this is needed

The current rule-based pipeline works as a baseline, but its accuracy on the Darija dataset is limited.

AtlasChat performs better, but we also want to test smaller transformer models that can be fine-tuned directly on our grievance categories.

## Models

### AraBERT

AraBERT is a pretrained Arabic BERT model.

It is expected to perform better on:

- Modern Standard Arabic
- formal complaints
- administrative text
- legal or official wording

### DarijaBERT

DarijaBERT is a pretrained BERT model for Moroccan Darija.

It is expected to perform better on:

- Moroccan Darija
- informal complaints
- local expressions
- non-standard spelling

## Dataset needed

The dataset should contain around 600 labeled grievance transcriptions.

Each row should include:

- text
- category
- urgency if available

Example:

```json
{"text": "بغيت نشكي على الزبالة ما تزادتش من الزنقة", "category": "services_municipaux", "urgency": "منخفض"}
