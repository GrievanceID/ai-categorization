# Cross-Lingual Corpus & Fallback Research — v2

**Owner:** Mira  
**Component:** AI categorization, summarization, routing, and NLP preparation  
**Repository target:** `GrievanceID/ai-categorization`  


```text
/datasets_and_mapping.md
/data/lexicon/government_legal_lexicon_expanded_v2.csv
```

---

## 1. Purpose of this document

This document updates the Week 3 NLP-preparation work for the voice-based citizen grievance platform. The goal is to build a stronger cross-lingual foundation for Moroccan government, legal, and courtroom audio where speakers mix:

- Moroccan Darija
- Modern Standard Arabic / formal Moroccan court Arabic
- French administrative and legal terms
- Moroccan names, honorifics, and local institutional vocabulary

The project needs this because ASR models can produce a transcript, but the downstream AI layer still needs to understand the transcript, categorize the grievance, and route it to the correct institution.

---

## 2. Why the legal/government lexicon is necessary

The SNRT courtroom-style sample showed that Moroccan legal audio contains formulaic court phrases, proper names, legal charges, financial terms, numbers, and French/Darija code-switching. These are exactly the phrases that can cause serious downstream errors if the transcript is wrong.

Examples of sensitive terms from the sample:

| Intended legal phrase | Why it matters |
|---|---|
| باسم جلالة الملك | Court-opening formula; should not be corrupted |
| طبقا للقانون | Legal procedure phrase |
| نعلن عن افتتاح الجلسة | Court session opening |
| الملف عدد 12/2023 | Case identifier |
| المتهمون | Identifies accused persons |
| يؤازرهم الأستاذ | Indicates legal representation |
| جنحة غسل الأموال | Core charge: money laundering |
| الأفعال المنصوص عليها | Legal reference phrase |
| القانون الجنائي | Criminal code reference |
| شنو كتقول حول المنسوب إليك | Judge’s question to defendant |
| أنا بريء | Plea/defense response |
| سوابق / سبق الحكم عليك | Prior conviction context |
| الاتجار في المخدرات | Drug-trafficking charge/history |
| الحسابات البنكية / خمسة مليار | Financial evidence and amount |
| الأصول التجارية / العقارات / الشركات | Asset ownership indicators |

A simple ASR error can become a serious AI-routing error. For example, confusing **خمسة مليار** with **خمسمائة مليار** changes the financial meaning of the case. Confusing **المنسوب إليك** with another phrase weakens legal summarization. Confusing **الأستاذ بشعيب** affects speaker/person extraction.

---

## 3. Open-source data audit: what exists and what is missing

### Existing useful resources

| Resource | Usefulness | Limitation for our project |
|---|---|---|
| DODa / Darija Open Dataset | Darija text and translation coverage; useful for general Darija normalization | Not a legal/government grievance-routing corpus |
| DODa-audio-dataset | 12,743 parallel Moroccan Darija text/speech samples | General-purpose; limited legal/admin vocabulary |
| Moroccan-Darija-Wiki-Audio-Dataset | 551 parallel Darija text/speech samples from Darija Wikipedia | Small and not courtroom/government specific |
| Moroccan-Darija-Wiki-Dataset | 10,044 parallel Darija text samples | Useful for language modeling, but not speech or legal routing |
| MoulSot-Full | Large Moroccan Darija speech resource; useful for ASR exploration | Still needs domain filtering for court/legal/government terms |
| Common Voice Arabic | Useful general Arabic speech reference | Standard Arabic does not replace Moroccan Darija for this use case |
| OPUS / JRC-Acquis / DGT / Europarl-style resources | Useful for French legal/administrative terminology and translation mapping | European legal language differs from Moroccan legal-admin speech |

### Research gap

Open-source Darija and Arabic resources exist, but no dedicated Moroccan Darija/French/Arabic **government grievance and courtroom corpus** was identified. The missing layer is not only transcription; it is a domain-specific mapping between:

```text
spoken Darija / Arabic / French term
→ normalized legal-admin term
→ complaint category
→ routing institution
→ confidence / human-review flag
```

---

## 4. Proposed cross-lingual mapping approach

The AI categorization pipeline should not depend only on one model. It should combine a lexicon, classification model, LLM reasoning, and human review.

### Step 1 — Normalize terminology

Map noisy ASR outputs and code-switched words to a clean normalized form.

Example:

```text
غسي الأموال / غسيل الاموال / blanchiment d'argent
→ غسل الأموال
→ category: financial_crime
```

### Step 2 — Extract administrative facts

From the transcript, extract:

- issue / charge / complaint topic
- people and roles: متهم، محامي، قاضي، شاهد، مشتكي
- location / institution
- document type: محضر، رخصة، شهادة، dossier, PV
- amount: درهم، سنتيم، مليون، مليار
- urgency and risk

### Step 3 — Categorize the case

Use a first-pass classifier such as DarijaBERT/AraBERT for fast category prediction:

- court/legal
- financial crime
- police/security
- civil registry
- municipal services
- land/property
- health
- education
- utilities
- social protection

### Step 4 — Use an LLM for summarization and routing reasoning

Use Atlas-Chat / LLM for:

- short case summary
- routing explanation
- ambiguity detection
- human-review recommendation

### Step 5 — Apply human review for sensitive or low-confidence outputs

Automatic routing should be blocked or flagged when:

- financial amounts are uncertain
- multiple institutions are possible
- speaker role is unclear
- legal charge is ambiguous
- the case contains sensitive identity/voice data

---

## 5. Recommended lexicon schema

The expanded CSV uses this schema:

| Column | Meaning |
|---|---|
| `term_original` | Term as it may appear in Arabic, Darija, or French |
| `language` | Language/style: Arabic/MSA, Darija, French, mixed, proper name |
| `normalized_form` | Clean canonical form used by NLP pipeline |
| `english_meaning` | English gloss for team readability |
| `category_hint` | Category signal for classifier/routing |
| `routing_hint` | Suggested institution/domain |
| `priority_hint` | Importance for correction: high/medium/low |
| `common_asr_errors_or_variants` | Likely ASR mistakes or spelling variants |
| `notes` | Why the term matters |
| `example_sentence` | Optional example usage |

---

## 6. What the custom dataset must cover

The team’s custom dataset should intentionally include:

1. **Court-opening and legal-procedure formulas**  
   Example: باسم جلالة الملك، طبقا للقانون، افتتاح الجلسة

2. **Defendant/charge structures**  
   Example: المتهم، جنحة، جناية، المنسوب إليك، الأفعال المنصوص عليها

3. **Financial crime vocabulary**  
   Example: غسل الأموال، حسابات بنكية، تحويلات، أصول تجارية، عقارات، شركات، فواتير

4. **Drug/legal-crime vocabulary**  
   Example: الاتجار في المخدرات، سوابق قضائية، حبس نافذ

5. **French legal/admin code-switching**  
   Example: plainte, réclamation, tribunal, audience, avocat, juge, dossier, PV, blanchiment d’argent

6. **Moroccan government-routing vocabulary**  
   Example: الجماعة، المقاطعة، العمالة، الحالة المدنية، المحافظة العقارية، الدرك، الأمن الوطني

7. **Names and honorifics**  
   Example: السي فؤاد، الأستاذ بشعيب، أمين، إدريس كبور

8. **Numbers and money expressions**  
   Example: مليون، مليار، سنتيم، درهم، خمسة مليار

---

## 7. Immediate next steps for Mira’s NLP prep

1. Upload the expanded lexicon CSV to:

```text
data/lexicon/government_legal_lexicon_expanded_v2.csv
```

2. Keep collecting WhisperX/MoulSot/Whisper errors in an error-analysis file:

```text
data/error_analysis/asr_legal_errors.csv
```

Suggested columns:

```text
audio_id,start_time,end_time,model_output,correct_text,error_type,priority,notes
```

3. Add correction candidates to the lexicon whenever repeated errors appear.

4. Build a small evaluation set with 50–100 legal/government utterances and a gold category/routing label.

5. Use the lexicon first for post-processing and later as seed data for classification/routing.

---

## 8. Main finding

General Moroccan Darija resources exist, but the project needs a specialized legal/government lexicon and custom evaluation set. The strongest contribution is a cross-lingual bridge that connects Darija, Arabic, and French legal-government expressions to downstream grievance categorization and routing.

---

## 9. Source links for dataset audit

- DODa-audio-dataset: https://huggingface.co/datasets/atlasia/DODa-audio-dataset
- Moroccan-Darija-Wiki-Audio-Dataset: https://huggingface.co/datasets/atlasia/Moroccan-Darija-Wiki-Audio-Dataset
- Moroccan-Darija-Wiki-Dataset: https://huggingface.co/datasets/atlasia/Moroccan-Darija-Wiki-Dataset
- MoulSot-Full: https://huggingface.co/datasets/atlasia/MoulSot-Full
- Mozilla Common Voice datasets: https://commonvoice.mozilla.org/en/datasets
- Moroccan Arabic Common Voice localization discussion: https://discourse.mozilla.org/t/moroccan-arabic-localization-request/82757
- OPUS corpus: https://opus.nlpl.eu/
- JRC-Acquis legal corpus paper: https://arxiv.org/abs/cs/0609058
