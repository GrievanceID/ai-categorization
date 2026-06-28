# Chikaya Routing Alignment Test Cases v1

## Purpose

This file tests whether our grievance categories can be mapped correctly to Chikaya-style sectors and likely destinations.

The goal is to check:

- the grievance category
- the Chikaya sector
- the likely destination
- whether human review is needed

---

## Test Case 1 — Health complaint

Transcript:

المستشفى ما بغاوش يستقبلو الوالدة وهي عندها حالة مستعجلة

Expected our category:

health

Expected Chikaya sector:

الصحة

Expected likely destination:

وزارة الصحة / المديرية الجهوية للصحة / المستشفى المعني

Human review:

yes

Reason:

The complaint mentions a hospital and an emergency health situation.

---

## Test Case 2 — Municipal services complaint

Transcript:

بغيت نشكي على الزبالة ما تزادتش من الزنقة ديالنا جوج سيمانات

Expected our category:

municipal_services

Expected Chikaya sector:

الجماعات الترابية

Expected likely destination:

الجماعة أو المقاطعة المعنية

Human review:

no

Reason:

The complaint is about local garbage collection.

---

## Test Case 3 — Civil registry complaint

Transcript:

مشيت نخرج عقد الازدياد ولكن مكتب الحالة المدنية قالو ليا الملف باقي ما وجدش

Expected our category:

civil_registry

Expected Chikaya sector:

الداخلية

Expected likely destination:

الجماعة الترابية / مكتب الحالة المدنية

Human review:

maybe

Reason:

The complaint concerns a civil registry document handled by local administration.

---

## Test Case 4 — Financial crime / legal complaint

Transcript:

أنا بريء من جنحة غسل الأموال وما عنديش علاقة بالحسابات البنكية اللي قالو عليها

Expected our category:

financial_crime

Expected Chikaya sector:

العدل

Expected likely destination:

وزارة العدل / النيابة العامة أو الجهة المختصة بالتحقيق المالي

Human review:

yes

Reason:

The complaint mentions money laundering and bank accounts, so it is legally sensitive.

---

## Test Case 5 — Land/property complaint

Transcript:

عندي مشكل فالرخصة ديال البناء والجماعة بقات كتسيفطني للمحافظة العقارية

Expected our category:

land_property

Expected Chikaya sector:

الاسكان والتعمير

Expected likely destination:

الوكالة الحضرية / المحافظة العقارية / الجماعة

Human review:

yes

Reason:

The complaint involves construction permit, commune, and land registry, so multiple institutions may be involved.

---

## Test Case 6 — Utilities complaint

Transcript:

الماء تقطع علينا ثلاثة أيام والفاتورة باقية طالعة

Expected our category:

utilities

Expected Chikaya sector:

البيئة والطاقة والمعادن

Expected likely destination:

المكتب أو المزود المسؤول عن الماء أو الكهرباء

Human review:

no

Reason:

The complaint concerns water service and billing.

---

## Test Case 7 — Labor/employment complaint

Transcript:

المشغل ما عطانيش الأجرة ديالي وما صرحش بيا ف CNSS

Expected our category:

labor_employment

Expected Chikaya sector:

التشغيل والتقاعد والتأمين الاجتماعي

Expected likely destination:

مفتشية الشغل / وزارة التشغيل / CNSS

Human review:

maybe

Reason:

The complaint involves salary and social insurance.

---

## Test Case 8 — Unclear complaint

Transcript:

ما فهمتش شنو وقع الملف مشا وبقاو كيقولو ليا سير ورجع

Expected our category:

unclear_needs_review

Expected Chikaya sector:

غير محدد

Expected likely destination:

مراجعة بشرية

Human review:

yes

Reason:

The transcript is unclear and should not be automatically routed.

---

## Notes

These test cases should be compared against:

- `data/routing/chikaya_routing_alignment_v1.csv`
- `src/baseline_grievance_classifier.py`
- Atlas-Chat outputs

The goal is to see whether our routing layer and Atlas-Chat can map complaints to the correct Chikaya-style sector.
