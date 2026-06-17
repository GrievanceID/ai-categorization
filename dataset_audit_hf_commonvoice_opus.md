# Dataset Audit: Moroccan Darija Legal/Government Data

## Purpose

This document is a separate audit file for the Week 3 task: **Cross-Lingual Corpus & Fallback Research**.

The goal is to check whether existing open-source datasets already contain Moroccan Darija legal, court, government, or administrative grievance data. This matters because our project is not a general Darija chatbot or general ASR system. It is a voice-based citizen grievance platform where people may speak in Moroccan Darija, Modern Standard Arabic, and sometimes French about courts, complaints, public institutions, money, documents, and administrative procedures.

---

## 1. Main Audit Result

Moroccan Darija datasets do exist on Hugging Face and related open-source platforms. However, based on public dataset cards and metadata, no reviewed dataset provides an explicitly labeled Moroccan Darija legal/government/court/grievance subset.

Therefore, the confirmed percentage of explicitly labeled Moroccan Darija legal/government data is:

**0% confirmed in public metadata / not measurable without manual annotation.**

This does **not** mean legal or government words never appear inside the datasets. It means the datasets do not provide domain labels that allow us to directly measure or extract a legal/government subset.

---

## 2. Hugging Face Audit

| Resource | Type | What it provides | Domain relevance | Legal/government percentage |
|---|---|---|---|---|
| MoulSot / MoulSot-Full | Moroccan Darija speech / ASR | Large Moroccan Darija speech resource; MoulSot-Full is reported as 1,500 hours total, with about 80 hours curated/transcribed | Very useful for Darija ASR and code-switching, but not labeled as legal/government | Not measurable from metadata; 0% explicitly labeled |
| DODa-audio | Moroccan Darija speech/text | 12,743 Darija speech/text samples with Arabic script, Latin script, and English translations | Useful for general Darija ASR/NLP | Not measurable from metadata; 0% explicitly labeled |
| Moroccan-Darija-Wiki-Audio | Darija speech/text | 551 speech/text samples from Darija Wikipedia | Useful for general Darija speech, not court/government grievances | Not measurable from metadata; 0% explicitly labeled |
| Moroccan-Darija-Wiki Dataset | Darija text | 10,044 Darija text samples from Wikipedia | Useful for general Darija NLP, not legal grievance routing | Not measurable from metadata; 0% explicitly labeled |
| DODa / Darija Open Dataset | Darija text/translation | More than 10,000 Darija entries for NLP and translation | Useful for general Darija vocabulary, spelling variation, and translation | Not measurable from metadata; 0% explicitly labeled |
| DarijaBanking | Moroccan Darija intent dataset | Domain-specific Moroccan Darija intent data | Useful example of how to build a domain-specific Darija classification dataset, but banking is not court/government grievance routing | Finance-domain only, not legal/government |

---

## 3. Mozilla Common Voice Audit

Mozilla Common Voice provides Arabic speech data, but the public Arabic dataset is not the same as Moroccan Darija.

The Common Voice Arabic dataset can be useful as a general Arabic ASR reference. However, for this project, it cannot be treated as a Moroccan Darija legal/government dataset because:

- It is labeled broadly as Arabic, not Moroccan Darija legal/government speech.
- It does not provide a clearly separated Moroccan Darija subset in the public metadata.
- It does not provide a court, legal, administrative, or grievance-routing domain label.
- Standard Arabic speech does not represent Moroccan Darija pronunciation, vocabulary, and code-switching patterns.

Therefore, the confirmed Moroccan Darija legal/government percentage in Common Voice Arabic is also:

**0% confirmed in public metadata / not measurable without manual annotation.**

---

## 4. OPUS / French Legal Data Audit

OPUS is useful for the French side of our project because Morocco often uses French in legal and administrative settings.

The most relevant OPUS source for legal structure is **JRC-Acquis**, a multilingual parallel corpus of mostly legal European Union documents. It is useful for mining French legal and administrative terminology such as:

- dossier
- plainte
- réclamation
- tribunal
- audience
- avocat
- juge
- procès-verbal / PV
- blanchiment d’argent
- société
- compte bancaire
- biens immobiliers
- autorisation
- attestation
- préfecture
- commune
- service public

However, OPUS/JRC-Acquis is **not Moroccan Darija** and **not Moroccan court audio**. It should be used as a French legal terminology source and translation-alignment support, not as a direct replacement for Moroccan legal/government speech data.

---

## 5. Darija/French/Arabic Translation Mapping System

To support code-switching, the project should use a mapping layer that connects the same legal/government concept across Moroccan Darija, formal Arabic, and French.

| Concept | Darija / Moroccan usage | Formal Arabic | French | Routing relevance |
|---|---|---|---|---|
| Complaint | شكاية / بغيت نشكي | شكاية / تظلم | plainte / réclamation | General grievance intake |
| Court | المحكمة | المحكمة | tribunal | Justice/legal routing |
| Hearing | الجلسة | الجلسة | audience | Court/legal context |
| Lawyer | الأستاذ / المحامي | المحامي | avocat | Legal actor |
| Accused person | المتهم | المتهم | accusé / prévenu | Criminal case |
| Money laundering | غسيل الأموال | غسل الأموال | blanchiment d’argent | Financial/legal category |
| Case file | ملف / دوسي | ملف | dossier | Case tracking |
| Police report | محضر / PV | محضر | procès-verbal / PV | Evidence/document handling |
| Bank account | الحساب البنكي | الحساب البنكي | compte bancaire | Financial evidence |
| Real estate | العقار / العمارات | العقارات | biens immobiliers | Asset investigation |
| Company | الشركة | الشركة | société | Business/financial routing |
| Permit | رخصة | رخصة | autorisation / permis | Administrative routing |
| National ID | البطاقة الوطنية | البطاقة الوطنية للتعريف | carte nationale / CIN | Identity/document routing |
| Birth certificate | عقد الازدياد | عقد الازدياد | acte de naissance | Civil registry routing |
| Municipality | الجماعة / الكومين | الجماعة | commune | Municipal routing |
| Prefecture | العمالة | العمالة | préfecture | Local administration routing |

---

## 6. Research Gap

The key gap is not simply “lack of Darija data.” The real gap is the lack of an open, labeled Moroccan Darija legal/government grievance corpus that includes:

- Moroccan court vocabulary
- government and administrative terms
- Darija/MSA/French code-switching
- Moroccan names, titles, and honorifics
- legal charges such as money laundering
- numbers and financial amounts
- routing categories linked to Moroccan institutions
- ASR correction pairs from real Moroccan legal/government audio

---

## 7. Project Implication

Because no reviewed dataset provides an explicitly labeled Moroccan Darija legal/government grievance subset, our custom lexicon and WhisperX correction candidates are necessary.

They fill the gap between general Darija ASR/NLP resources and the real requirements of a Moroccan voice-based citizen grievance platform.

Our project should therefore continue building:

1. A Moroccan legal/government lexicon.
2. A WhisperX/ASR correction candidate list.
3. A cross-lingual mapping layer for Darija, formal Arabic, and French.
4. A small manually verified dataset from real Moroccan legal/government audio.
5. Classification labels connected to Moroccan public institutions and grievance-routing categories.
