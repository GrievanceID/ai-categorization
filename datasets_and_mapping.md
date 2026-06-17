
# Cross-Lingual Corpus & Fallback Research

**Project:** SURP'26 — Voice-Based Citizen Grievance Platform  
**Repository:** `GrievanceID/ai-categorization`  
**Prepared by:** Amira / Mira  
**Week:** 3  

---

## 1. Objective

This document audits open-source Moroccan Darija / Arabic / French data sources that could support the AI categorization and routing layer of a voice-based citizen grievance platform.

My specific goal is to answer:

1. What open-source Moroccan Darija data already exists?
2. Does any of it contain legal, government, administrative, or grievance-related content?
3. Can French legal/government corpora help with code-switched Darija/French grievances?
4. What dataset and mapping system should our custom pipeline build next?

---

## 2. Executive Summary

Open-source Moroccan Darija resources exist, but most are general-purpose: social media, Wikipedia, translation pairs, banking intent detection, or generic speech samples. I did **not** find a dedicated open-source Moroccan Darija legal/government grievance corpus that directly matches our use case.

The main research gap for our project is therefore not only “Darija speech-to-text.” The gap is **Darija/French/Arabic government-context understanding**: extracting administrative meaning, categorizing complaints, and routing them to the correct public institution.

For this reason, our custom dataset should focus on:

- Moroccan government/legal vocabulary
- Proper names and honorifics such as `السي`, `سيدي`, `الأستاذ`, `السيدة`
- French administrative terms used in Moroccan speech
- Darija number expressions
- Complaint categories aligned with Moroccan public services
- Routing labels linked to institutions or departments

---

## 3. Dataset Audit: Moroccan Darija Sources

| Source | Type | Useful for our project? | Limitation for our use case |
|---|---|---|---|
| `atlasia/Atlaset` | Large Moroccan Darija text corpus | Useful for pretraining/background Darija language understanding | Not specifically legal/government grievance data |
| `atlasia/DODa-audio-dataset` | Darija speech + text samples | Useful for Darija ASR and transcript normalization | General Darija, not government-domain specific |
| `atlasia/Moroccan-Darija-Wiki-Audio-Dataset` | Darija Wikipedia audio/text | Useful for clean Darija speech and text pairs | Encyclopedic style, not complaint/legal style |
| DODa / Darija Open Dataset | Darija-English lexical/translation resource | Useful for Darija spelling variants and lexicon building | Mostly general vocabulary, not routing labels |
| DarijaBERT | Moroccan Darija BERT model | Useful for classification experiments | Needs task-specific labeled grievance data |
| Atlas-Chat | Darija LLM | Useful for summarization and routing reasoning | Needs controlled prompts and human validation |
| DarijaBanking | Banking intent dataset | Good example of domain-specific Darija intent classification | Domain is banking, not government grievances |
| DVOICE / Darija voice data | Community voice data | Useful for ASR/speaker research | Not focused on legal/government vocabulary |
| Mozilla Common Voice Arabic | Arabic speech data | Useful for MSA speech baseline | Arabic dataset is not Moroccan-Darija-specific |

### Key finding

Open-source data can support **general Darija understanding**, but our project still needs a custom domain layer for **legal/government grievance vocabulary and routing labels**.

---

## 4. Estimated Coverage of Moroccan Darija Legal/Government Data

Because the audited datasets do not provide a direct “legal/government grievance” percentage label, an exact statistical percentage cannot be claimed honestly without downloading and classifying every row.

However, based on dataset descriptions:

- **Dedicated Moroccan Darija legal/government grievance corpus found:** 0
- **Dedicated Moroccan Darija public-service routing corpus found:** 0
- **General Darija text/speech datasets found:** yes
- **French legal/government parallel corpora found:** yes, but they are mostly EU/French institutional text, not Moroccan Darija

### Practical conclusion

For our research report, we can say:

> The current open-source ecosystem contains general Moroccan Darija speech and text resources, but no clearly dedicated open-source Moroccan Darija legal/government grievance dataset was identified. Therefore, our custom contribution is to build a small domain-specific dataset and mapping layer for Moroccan public-service complaints.

---

## 5. French Legal/Government Data from OPUS

OPUS contains large multilingual corpora that can support French legal or administrative terminology. These are useful because Moroccan complaints often contain French code-switching, especially for institutions, documents, legal terms, and public services.

Potential OPUS corpora to inspect:

| OPUS Corpus | Why it matters |
|---|---|
| JRC-Acquis | EU legal texts; useful for formal legal terminology |
| DGT | Translation memory from EU institutions; useful for administrative and legal phrasing |
| Europarl | Parliamentary debates; useful for formal institutional language |
| EUbookshop | Public policy/government-like documents |
| EMEA | Medical/health terminology, useful for health complaints |
| MultiUN / UNPC | Formal international institutional language |

### Limitation

These corpora are not Moroccan Darija. They should not be used as direct training data for Darija classification without adaptation. Their best use is to help build:

- French legal/admin term list
- French → Arabic/MSA → Darija mapping
- Code-switching normalization rules
- Institutional vocabulary for routing categories

---

## 6. Proposed Translation & Mapping System

The goal is to handle code-switched grievances where a citizen mixes Darija, Arabic, and French.

### Example problem

A citizen may say:

> “عندي مشكل فـ dossier ديال permis، مشيت للمقاطعة ولكن قالو ليا système طايح.”

The system should understand:

- `dossier` = administrative file
- `permis` = permit/license
- `المقاطعة` = local administrative office / district authority
- `système طايح` = system down / service unavailable
- likely category = municipal / administrative service
- possible routing = local commune / district office

---

## 7. Proposed Lexicon Schema

Create a file called `government_legal_lexicon.csv` or `lexicon.md` with the following fields:

| Field | Description | Example |
|---|---|---|
| `term_original` | The word/phrase as spoken/written | `dossier` |
| `language` | Darija / MSA / French / mixed | French |
| `normalized_form` | Clean normalized version | `ملف إداري` |
| `english_meaning` | Simple English meaning | administrative file |
| `category_hint` | Suggested complaint category | civil registry / municipal services |
| `routing_hint` | Suggested institution type | commune / local office |
| `example_sentence` | Example grievance sentence | `بغيت نعرف فين وصل dossier ديالي` |
| `priority_hint` | low / medium / high | medium |
| `notes` | Ambiguity or context note | could also mean school file |

---

## 8. Initial Lexicon Seeds

| Term | Language | Normalized meaning | Category hint | Routing hint |
|---|---|---|---|---|
| `السي` | Darija honorific | Mr. / respectful address | general | none |
| `سيدي` | Darija/MSA honorific | Sir | general | none |
| `محكمة` | Arabic/Darija | court | justice/legal | court/justice office |
| `شكاية` | Arabic/Darija | complaint | general grievance | complaint portal |
| `رخصة` / `permis` | Arabic/French | license/permit | transport/municipal/admin | commune or transport authority |
| `dossier` | French | administrative file | civil registry/admin | local office |
| `acte de naissance` | French | birth certificate | civil registry | commune/civil registry office |
| `carte nationale` | French/Arabic context | national ID card | identity/civil registry | identity administration |
| `المقاطعة` | Darija/MSA | district/local office | municipal services | local commune/district |
| `الجماعة` | Arabic/Darija | commune/municipality | municipal services | commune |
| `الماء` | Darija/MSA | water | utilities | water utility |
| `الضو` | Darija | electricity | utilities | electricity utility |
| `الزبالة` | Darija | garbage/waste | municipal services | commune/waste service |
| `السبيطار` | Darija | hospital | health | health authority/hospital |
| `المدرسة` | Arabic/Darija | school | education | school/education delegation |
| `تعويض` | Arabic/Darija | compensation/payment | social protection | social services |
| `استدعاء` | Arabic/Darija | summons/notice | justice/admin | relevant institution |
| `مقدم` | Moroccan admin term | local authority officer | local administration | local authority |
| `قائد` | Moroccan admin term | local authority leader | local administration | caidat/local authority |
| `بروسي` / `PV` | Darija/French | official report/minutes | legal/admin | police/court/admin |

---

## 9. Classification and Routing Categories

Suggested initial taxonomy:

1. Civil registry and identity documents
2. Municipal services
3. Health
4. Education
5. Transport
6. Utilities: water, electricity, sanitation
7. Justice/legal
8. Social protection
9. Housing/land
10. Police/security
11. Taxes/fees
12. Other / unclear

Each category should have:

- label name
- examples
- institution type
- keywords
- confidence threshold
- human-review rule

---

## 10. Proposed NLP Pipeline for Mira’s Component

Input from Lina:

```json
{
  "audio_id": "clip_01",
  "segments": [
    {"speaker": "Citizen", "start": 0.0, "end": 8.2, "text": "..."},
    {"speaker": "Agent", "start": 8.3, "end": 11.5, "text": "..."}
  ]
}
```

Mira’s processing steps:

1. **Normalize text**
   - standardize spelling variants
   - identify French/Darija/MSA terms
   - preserve names and numbers carefully

2. **Extract key fields**
   - issue
   - location
   - date/duration
   - institution mentioned
   - prior action
   - urgency
   - evidence

3. **Categorize complaint**
   - DarijaBERT/AraBERT for fast classification
   - Atlas-Chat for reasoning when the case is complex

4. **Route complaint**
   - map category to institution type
   - add confidence score
   - flag unclear cases for human review

5. **Produce structured JSON**

```json
{
  "summary": "Citizen reports a delay in receiving an administrative permit from the local office.",
  "category": "civil_registry_or_municipal_services",
  "urgency": "medium",
  "institution_type": "local commune / district office",
  "evidence": ["mentions dossier", "mentions local office", "mentions system down"],
  "confidence": 0.74,
  "human_review_required": true
}
```

---

## 11. Fallback Research Strategy

Because Darija government data is limited, we should use a fallback strategy:

### Level 1 — Use existing Darija resources
Use Atlaset, DODa, DODa-Audio, DarijaBERT, Atlas-Chat, and DarijaBanking to support general Darija understanding.

### Level 2 — Use French legal/government corpora
Use OPUS corpora like JRC-Acquis, DGT, Europarl, and EMEA to build French administrative/legal vocabulary.

### Level 3 — Build our custom mini-dataset
Use the team’s SNRT/courtroom clips and manual transcripts to create domain-specific examples.

### Level 4 — Human-in-the-loop review
When confidence is low, do not auto-route. Send to human review.

---

## 12. Research Gap Statement

Existing Moroccan Darija datasets are useful for general language modeling, ASR, and translation, but they do not directly cover the government grievance workflow. French legal corpora exist, but they do not reflect Moroccan Darija code-switching or Moroccan institutional routing.

Our project fills this gap by creating a pipeline that combines:

- Darija/Arabic/French transcript understanding
- government/legal lexicon mapping
- complaint categorization
- routing to the right institution
- confidence scoring and human review
- later integration with the MOSIP/Inji trust layer

---

## 13. Next Steps for My Repository

1. Add this file to `GrievanceID/ai-categorization` as:

```bash
datasets_and_mapping.md
```

2. Create a `data/lexicon/` folder.
3. Start `government_legal_lexicon.csv` using the schema above.
4. Create 10–20 mock grievance examples with labels.
5. Define the first routing taxonomy in `data/taxonomy/chikaya_style_taxonomy.md`.

---

## 14. Sources to Track

- Hugging Face Moroccan Darija dataset collections
- Atlaset dataset card
- DODa / Darija Open Dataset paper
- DarijaBERT Hugging Face model card
- Atlas-Chat paper
- DarijaBanking paper
- DVOICE / Darija voice dataset
- Mozilla Common Voice Arabic and Moroccan Darija localization discussions
- OPUS corpora: JRC-Acquis, DGT, Europarl, EMEA, EUbookshop, MultiUN/UNPC

---

## 15. One-Sentence Contribution

My contribution is to document the lack of a dedicated Moroccan Darija government-grievance corpus and propose a cross-lingual mapping layer that connects Darija, Arabic, and French expressions to complaint categories, routing decisions, and human-review safeguards.
