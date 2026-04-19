# 01 PDF Extraction
Instructions for extracting text and data from agricultural PDF sources.
# Skill 01 — PDF & Document Extraction

Use this when working on source acquisition and content extraction from agricultural extension PDFs.

---

## Data Sources

| # | Source | Access | Language | Est. Yield |
|---|--------|--------|----------|-----------|
| 1 | KALRO Extension Pamphlets | Public — kalro.org/publications | SW & EN | 500–800 pairs |
| 2 | FAO Swahili Publications | Public — fao.org document repository | SW | 300–500 |
| 3 | Plantwise/CABI Knowledge Bank | Public — plantwise.org | EN (translate) | 400–600 |
| 4 | CABI Swahili Pest Guides | Public — bioprotectionportal.com | SW | 200–300 |
| 5 | Extension Officer Training Manuals | Semi-public — county ag offices | SW & EN | 200–300 |

**Search terms for FAO**: "Kiswahili", "farmer field school", "IPM", "pest management"

---

## PDF Classification

Before extracting any PDF, classify it:

- **Native text**: pymupdf extracts >100 chars/page on average → use pymupdf text extraction
- **Scanned/image**: pymupdf returns empty or garbage text → use tesseract OCR with `swa+eng` langpack
- **Mixed**: some pages native, some scanned → hybrid per-page approach

**OCR quality check**: If average word length < 2.5 characters after OCR, the extraction likely failed. Flag for manual review. If Swahili language detection < 0.5, try English-only OCR.

---

## Cataloging Rule

Every downloaded source file gets logged to `dataset/raw/sources/source_inventory.jsonl` with:

- filename
- URL
- access_date (YYYY-MM-DD)
- SHA256 hash
- file_size_bytes
- language (sw/en/mixed)
- source_type

Never modify original files. Work from copies.

---

## Segmentation

Raw extracted text must be broken into **atomic advisory segments** — one pest/disease + one crop + one actionable advisory per segment.

**Segmentation rules:**
1. One segment = one question a farmer might ask
2. Two different pests on same crop in one paragraph → split into two segments
3. One pest across multiple crops → keep as one segment, note all crops
4. Discard: table of contents, bibliography, headers/footers, page numbers, publisher info
5. Minimum segment length: 50 characters
6. Maximum segment length: 2000 characters (split longer ones)

**Swahili section headers to look for**: "Wadudu" (insects), "Magonjwa" (diseases), "Magugu" (weeds), "Udhibiti" (control/management)

Use LLM for first-pass segmentation, then human review for agricultural accuracy.

---

## KALRO-Specific Extraction Notes

KALRO pamphlets typically follow: Title page → Table of contents → Introduction → Pest/disease sections → Appendices

- Skip title page and ToC
- Introduction may have useful context — mark as `general` segment type
- Pest/disease sections are the PRIMARY target, usually structured as: Name → Symptoms → Damage → Management
- Appendices may have useful reference tables

---

## FAO Farmer Field School Guide Notes

Structured as exercises/lessons. Extract:
- Problem descriptions from lesson content
- Management recommendations from "what to do" sections
- Skip: facilitator instructions, group activity descriptions, assessment questions

---

## Plantwise Fact Sheet Notes

Highly structured — each fact sheet = one pest on one crop:
- Symptoms section → basis for farmer question construction
- Management section → becomes the answer
- Usually English → flag for translation in QA construction phase

---

## Output

Each extracted segment → one JSONL record in `dataset/raw/extracted/` with fields: segment_id, source_file, source_ref, source_type, page_num, segment_text, crop_detected, pest_disease_detected, segment_type (diagnosis/treatment/prevention/general), language, extraction_method, extracted_date

---

## Dependencies

System: `tesseract-ocr`, `tesseract-ocr-swa`, `poppler-utils`
Python: `pymupdf`, `pdf2image`, `pytesseract`, `Pillow`, `fasttext`

---

## Failure Modes

| Failure | Detection | Fix |
|---------|-----------|-----|
| OCR produces gibberish | Avg word length < 2.5 | Increase DPI to 400, try eng only, manual extraction |
| Headers/footers in segments | Repeated identical text across segments | Strip first/last 2 lines if matching across 3+ pages |
| Tables extracted as garble | Irregular spacing | Use tabula-py for tables, or extract manually |
| Bilingual text mixed | Language detection oscillates | Split by paragraph, detect language per paragraph |
| PDF is password-protected | fitz.open() errors | Skip, log, find alternative source |