# ShambaQA Project Instructions
This file contains foundational mandates for the Gemini CLI when working within this project.
# ShambaQA — Gemini CLI Instructions

You are building **ShambaQA**, a Swahili Agricultural Pest & Disease Advisory QA dataset for the Uncharted Data Challenge. **Deadline: April 27, 2026.**

---

## What This Is

An open-source QA dataset in Swahili covering crop pest/disease diagnostics for East African smallholder farmers. Zero equivalent datasets exist anywhere.

---

## Project Directory

```
shambaqa/
├── GEMINI.md
├── .gemini/
│   └── skills/
│       ├── 01_pdf_extraction.md
│       ├── 02_transcription.md
│       ├── 03_qa_construction.md
│       ├── 04_annotation_validation.md
│       └── 05_dataset_release.md
├── dataset/
│   ├── raw/
│   │   ├── sources/                    ← Downloaded PDFs, audio files
│   │   │   └── source_inventory.jsonl  ← SHA256 + URL log per file
│   │   └── extracted/                  ← Text segments (JSONL per source)
│   ├── processed/
│   │   ├── shambaqa_v1.0.jsonl
│   │   ├── shambaqa_v1.0.csv
│   │   ├── train.jsonl
│   │   ├── dev.jsonl
│   │   └── test.jsonl
│   ├── metadata/
│   │   ├── crop_vocabulary.json
│   │   ├── pest_disease_vocab.json
│   │   ├── category_definitions.json
│   │   ├── annotation_stats.json
│   │   └── dataset_statistics.json
│   └── rejected/                       ← Failed validation records + reasons
├── scripts/
│   ├── extract/
│   │   ├── catalog_source.py
│   │   ├── extract_pdf.py
│   │   ├── segment_text.py
│   │   └── transcribe_audio.py
│   ├── process/
│   │   ├── construct_qa_pairs.py
│   │   ├── deduplicate.py
│   │   ├── validate_schema.py
│   │   ├── compute_splits.py
│   │   └── translate_pairs.py
│   ├── analyze/
│   │   ├── dataset_statistics.py
│   │   ├── iaa_scores.py
│   │   ├── baseline_classification.py
│   │   ├── baseline_afroxlmr.py
│   │   └── learning_curve.py
│   └── requirements.txt
├── docs/
│   ├── annotation_guidelines.md
│   ├── severity_rubric.md
│   ├── edge_cases.md
│   └── source_inventory.md
├── examples/
│   ├── load_dataset.py
│   ├── fine_tune_qa.py
│   └── explore_dataset.ipynb
├── README.md
├── METHODOLOGY.md
├── DATA_DICTIONARY.md
├── RESPONSIBLE_USE.md
├── CITATION.cff
├── CHANGELOG.md
├── LICENSE
├── requirements.txt
├── smoke_test.sh
└── .gitignore
```

---

## Skill Routing

Read the relevant skill file BEFORE starting any phase:

| Task | Read First |
|------|-----------|
| PDF download, OCR, text extraction | `.gemini/skills/01_pdf_extraction.md` |
| Audio/video transcription | `.gemini/skills/02_transcription.md` |
| QA pair construction & augmentation | `.gemini/skills/03_qa_construction.md` |
| Labeling, IAA, dedup, validation | `.gemini/skills/04_annotation_validation.md` |
| Splits, baselines, docs, release | `.gemini/skills/05_dataset_release.md` |

---

## Schema — Every QA Record

| Field | Type | Nullable |
|-------|------|----------|
| `id` | string (`shambaqa-XXXXX`) | NO |
| `question_sw` | string (Swahili question) | NO |
| `answer_sw` | string (Swahili answer) | NO |
| `question_en` | string (English translation) | YES |
| `answer_en` | string (English translation) | YES |
| `crop` | string (controlled vocab) | NO |
| `crop_en` | string | YES |
| `pest_disease` | string (controlled vocab) | NO |
| `pest_disease_en` | string | YES |
| `pest_disease_scientific` | string | YES |
| `category` | enum (11 values) | NO |
| `severity` | enum (`low`/`medium`/`high`/`critical`) | NO |
| `region` | string | YES |
| `source_type` | enum | NO |
| `source_ref` | string (specific citation) | NO |
| `question_source` | enum | NO |
| `dialect_variant` | enum | NO |
| `confidence` | float 0.0–1.0 | NO |
| `annotator_id` | string (`ann-XX`) | NO |
| `review_status` | enum | NO |
| `created_date` | date (`YYYY-MM-DD`) | NO |

---

## Enums

**category** (exactly 11): `fungal_disease`, `bacterial_disease`, `viral_disease`, `insect_pest`, `mite`, `nematode`, `weed`, `nutrient_deficiency`, `abiotic_stress`, `storage_pest`, `general_management`

**severity**: `low`, `medium`, `high`, `critical`

**source_type**: `extension_pamphlet`, `radio_transcript`, `faq`, `expert_written`, `field_report`

**question_source**: `constructed_from_pattern`, `adapted_from_transcript`, `direct_from_source`

**dialect_variant**: `kenyan_swahili`, `tanzanian_swahili`, `standard`

**review_status**: `draft`, `reviewed`, `validated`, `disputed`

---

## Priority Crops (12)

| Swahili | English | Scientific |
|---------|---------|-----------|
| Mahindi | Maize | *Zea mays* |
| Maharage | Beans | *Phaseolus vulgaris* |
| Mpunga | Rice | *Oryza sativa* |
| Ngano | Wheat | *Triticum aestivum* |
| Viazi | Potatoes | *Solanum tuberosum* |
| Nyanya | Tomatoes | *Solanum lycopersicum* |
| Vitunguu | Onions | *Allium cepa* |
| Kahawa | Coffee | *Coffea arabica* |
| Chai | Tea | *Camellia sinensis* |
| Ndizi | Bananas | *Musa spp.* |
| Mihogo | Cassava | *Manihot esculenta* |
| Mtama | Sorghum | *Sorghum bicolor* |

---

## Quality Gates

Do NOT proceed past a gate until it passes:

- **GATE 1** (after source acquisition): Estimated yield ≥ 1,200 QA pairs from accessible sources. If not, escalate.
- **GATE 2** (after annotation calibration): IAA — crop κ ≥ 0.90, category κ ≥ 0.80, severity weighted κ ≥ 0.70, pest_disease κ ≥ 0.75. If not, revise guidelines and re-calibrate.
- **GATE 3** (after validation): ≥ 1,500 unique QA pairs after dedup. If not, trigger stretch collection.
- **GATE 4** (final): Fresh clone → pip install → notebook runs → baselines reproduce ±0.02 F1.

---

## Hard Rules

1. **Source tracking**: `source_ref` must be specific. "KALRO materials" = rejected. "KALRO Maize IPM Guide 2023, pg. 12" = accepted.
2. **Language**: `question_sw` and `answer_sw` must pass Swahili detection > 0.9. Questions > 10 chars, Answers > 30 chars.
3. **Ethics**: No WHO Hazard Class Ia/Ib pesticides. No PII. No brand names. Informational only.
4. **Code standards**: Python 3.10+, seed=42 everywhere, JSONL for data, UTF-8, idempotent scripts, argparse on every script.
5. **Rejects**: Never silently drop data. Failed records go to `dataset/rejected/` with reasons.

---

## What "Done" Looks Like

- [ ] ≥ 1,500 validated QA pairs (target: 3,000)
- [ ] All 12 crops (min 50 each), all 11 categories (min 30 each)
- [ ] IAA scores computed and published
- [ ] Train/dev/test splits (80/10/10, stratified, no leakage)
- [ ] TF-IDF + AfroXLMR baselines with Macro F1
- [ ] README, DATA_DICTIONARY, METHODOLOGY, RESPONSIBLE_USE complete
- [ ] GitHub repo structured + HuggingFace Hub upload
- [ ] `explore_dataset.ipynb` runs end-to-end from fresh clone