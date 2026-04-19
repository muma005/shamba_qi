# Methodology
Details on the data collection, extraction, and QA generation process.
# ShambaQA Collection Methodology

This document describes how ShambaQA was collected, constructed, annotated, and validated. Every step is documented to enable reproduction.

---

## 1. Source Identification

Sources were selected based on three criteria: public accessibility, agricultural authority, and Swahili language availability.

| Source | Type | Access | Language | Est. Yield |
|--------|------|--------|----------|-----------|
| KALRO Extension Pamphlets | PDF/printed guides | Public — kalro.org | SW & EN | 500–800 pairs |
| FAO Swahili Publications | Farmer field school guides | Public — fao.org | SW | 300–500 |
| Plantwise/CABI Knowledge Bank | Pest fact sheets | Public — plantwise.org | EN (translated) | 400–600 |
| CABI Swahili Pest Guides | Translated pest guides | Public — bioprotectionportal.com | SW | 200–300 |
| Shamba Shape Up (Mediae) | TV show transcripts | Public broadcast — YouTube | SW | 200–400 |
| Agricultural Radio (KBC, Radio Citizen) | Call-in segment transcripts | Public broadcast | SW | 100–200 |
| Extension Officer Training Manuals | Training materials | Semi-public — county ag offices | SW & EN | 200–300 |

All source files are logged in `dataset/raw/sources/source_inventory.jsonl` with filename, URL, access date, and SHA256 hash.

---

## 2. Content Extraction

**PDFs** were classified as native text, scanned, or mixed. Native text PDFs were extracted using pymupdf. Scanned PDFs were OCR'd using tesseract with the Swahili language pack (`swa+eng`). OCR quality was logged per file — files with average word length below 2.5 characters were flagged for manual review.

**Audio/video** (Shamba Shape Up, radio) was transcribed using Whisper large-v3 with Swahili forced. An agricultural term corrections dictionary was applied to fix common Whisper errors on Swahili farming vocabulary. Segments with no-speech probability above 0.5 were filtered.

---

## 3. Segmentation

Extracted text was broken into atomic advisory segments — one pest/disease, one crop, one actionable advisory per segment. Segmentation was LLM-assisted with human review.

Segmentation rules:
- Each segment must be self-contained
- Two pests on same crop → two segments
- One pest across multiple crops → one segment, all crops noted
- Table of contents, headers, footers, publisher info discarded
- Minimum 50 characters, maximum 2000 characters per segment

---

## 4. QA Pair Construction

For each advisory segment, 2–3 question-answer pairs were constructed.

**Questions** follow four documented farmer communication patterns:
1. **Symptom description**: Farmer describes what they see on their crop
2. **Identification request**: Farmer asks to identify a pest/symptom
3. **Treatment request**: Farmer asks what to do about a known problem
4. **Prevention query**: Farmer asks how to prevent a problem

Questions were written in natural spoken Swahili (not formal/academic) by Swahili-native speakers using an LLM-assisted workflow: LLM generates draft questions → human reviewer corrects for naturalness and agricultural accuracy.

**Answers** are grounded in the source material. No information was added beyond what the source provides. Answers include both diagnosis and management recommendation when the source provides both.

**Direct-from-source pairs** from Shamba Shape Up and radio transcripts preserve the farmer's original question with minimal editing. These are marked with `question_source = "direct_from_source"`.

---

## 5. Translation

All Swahili QA pairs were translated to English (`question_en`, `answer_en`) using machine translation with manual correction. 50 random samples were spot-checked for translation quality.

Pest/disease names were mapped to scientific nomenclature using the CABI Crop Protection Compendium.

---

## 6. Annotation

Each QA pair was independently labeled by two annotators for: `crop`, `category`, `pest_disease`, `severity`, `dialect_variant`, and `confidence`.

Disagreements were resolved by a third adjudicator with agricultural expertise. Edge case decisions are documented in `docs/edge_cases.md`.

---

## 7. Quality Control

- **Inter-annotator agreement** was computed on a 200-pair calibration set. Required thresholds: crop κ ≥ 0.90, category κ ≥ 0.80, severity weighted κ ≥ 0.70, pest_disease κ ≥ 0.75. Full annotation did not begin until thresholds were met.
- **Domain expert spot-check**: 20% of the first 500 entries and 10% of the remainder were reviewed by an agricultural domain expert.
- **Automated validation**: every record passed `validate_schema.py` checking for null required fields, valid enums, string lengths, and Swahili language detection > 0.9.
- **Deduplication**: Jaccard similarity on tokenized questions. Pairs above 0.7 similarity were deduplicated (higher confidence retained). Borderline pairs (0.5–0.7) were manually reviewed.

---

## 8. Splitting

Train/dev/test splits were computed at 80/10/10 ratio, stratified by `crop` and `category`. QA pairs sharing the same `answer_sw` (from question augmentation) were kept in the same split to prevent data leakage. Random seed: 42.

---

## 9. Sampling

The dataset targets stratified coverage:
- All 12 priority crops represented (minimum 50 pairs each)
- All 11 categories represented (minimum 30 each)
- Both Kenyan and Tanzanian dialect variants (~65/10 split with 25% standard)
- Severity distribution targeting: low 25%, medium 40%, high 25%, critical 10%

---

## 10. Anonymization

- No real farmer PII was collected — questions are constructed or from public broadcast transcripts
- Speaker names from transcripts replaced with role tags [Farmer], [Expert]
- Annotator IDs are pseudonymized (ann-01, ann-02, etc.)
- Source references cite publications, not individuals

---

## Reproducibility

- All source files are cataloged with SHA256 hashes and access dates
- All scripts are included in `scripts/` with pinned dependencies
- Random seeds are fixed at 42 for all stochastic operations
- The pipeline is reproducible from `dataset/raw/extracted/` forward; reproduction from original sources depends on continued source availability