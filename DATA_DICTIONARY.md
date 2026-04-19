# Data Dictionary
Definitions for all fields in the dataset.
# ShambaQA Data Dictionary

This document defines every column in the ShambaQA dataset.

---

## Column Definitions

| Column | Type | Nullable | Description | Example |
|--------|------|----------|-------------|---------|
| `id` | string | NO | Unique identifier, format `shambaqa-XXXXX` | `shambaqa-00142` |
| `question_sw` | string | NO | Farmer question in Swahili | `Majani ya mahindi yangu yameanza kuwa na madoa ya kahawia, ni ugonjwa gani?` |
| `answer_sw` | string | NO | Expert answer in Swahili | `Hii inaweza kuwa ugonjwa wa blight ya majani. Ondoa majani yaliyoathiriwa na piga dawa ya fungicide.` |
| `question_en` | string | YES | English translation of question | `My maize leaves have started developing brown spots, what disease is this?` |
| `answer_en` | string | YES | English translation of answer | `This could be Northern Leaf Blight. Remove affected leaves and apply fungicide.` |
| `crop` | string | NO | Primary crop referenced (Swahili, from controlled vocabulary) | `mahindi` |
| `crop_en` | string | YES | Crop name in English | `maize` |
| `pest_disease` | string | NO | Identified pest or disease (Swahili, from controlled vocabulary) | `Blight ya majani ya kaskazini` |
| `pest_disease_en` | string | YES | Pest/disease English name | `Northern Leaf Blight` |
| `pest_disease_scientific` | string | YES | Scientific binomial name | `Exserohilum turcicum` |
| `category` | enum | NO | Problem category (see enum below) | `fungal_disease` |
| `severity` | enum | NO | Urgency level (see enum below) | `medium` |
| `region` | string | YES | Applicable geographic region | `Kenya - Central Highlands` |
| `source_type` | enum | NO | Source material category | `extension_pamphlet` |
| `source_ref` | string | NO | Specific source citation | `KALRO Maize IPM Guide 2023, pg. 12` |
| `question_source` | enum | NO | How the question was created | `constructed_from_pattern` |
| `dialect_variant` | enum | NO | Swahili dialect variant | `kenyan_swahili` |
| `confidence` | float | NO | Annotator confidence in labels, 0.0–1.0 | `0.85` |
| `annotator_id` | string | NO | Pseudonymized annotator identifier | `ann-03` |
| `review_status` | enum | NO | Quality review status | `validated` |
| `created_date` | date | NO | Date record was created (YYYY-MM-DD) | `2026-04-22` |

---

## Enum Definitions

### `category` (11 values)

| Value | Description |
|-------|-------------|
| `fungal_disease` | Diseases caused by fungi — blights, rusts, smuts, mildews, fungal wilts |
| `bacterial_disease` | Diseases caused by bacteria — bacterial wilts, cankers, soft rots |
| `viral_disease` | Diseases caused by viruses — mosaics, streaks, leaf curls |
| `insect_pest` | Damage from insects at any life stage |
| `mite` | Spider mites, eriophyid mites, broad mites |
| `nematode` | Plant-parasitic nematodes — root-knot, cyst, lesion |
| `weed` | Crop competition and parasitism from weeds including Striga |
| `nutrient_deficiency` | Symptoms from lack of essential nutrients, not pathogens |
| `abiotic_stress` | Non-living environmental damage — drought, waterlogging, frost |
| `storage_pest` | Post-harvest pests in stored grain/produce |
| `general_management` | General agriculture — crop rotation, soil prep, IPM, no specific pest |

### `severity` (4 values)

| Value | Yield Impact | Spread | Timeframe |
|-------|-------------|--------|-----------|
| `low` | <5% | None | Non-urgent |
| `medium` | 5–20% | Localized | Days to weeks |
| `high` | 20–50% | Spreading | Action needed this week |
| `critical` | >50% | Epidemic risk | Action needed today |

### `source_type` (5 values)

| Value | Description |
|-------|-------------|
| `extension_pamphlet` | KALRO, FAO, CABI printed/PDF guides |
| `radio_transcript` | Transcribed agricultural radio or TV segments |
| `faq` | Frequently asked questions from extension websites |
| `expert_written` | Content authored by agricultural experts for this dataset |
| `field_report` | Field observation reports from extension officers |

### `question_source` (3 values)

| Value | Description |
|-------|-------------|
| `direct_from_source` | Real farmer question from transcript (highest quality) |
| `adapted_from_transcript` | Cleaned/restructured exchange from transcript |
| `constructed_from_pattern` | Question generated from documented farmer communication patterns |

### `dialect_variant` (3 values)

| Value | Description |
|-------|-------------|
| `kenyan_swahili` | Kenyan dialect markers (e.g., "shamba" frequency, "mkulima") |
| `tanzanian_swahili` | Tanzanian dialect markers |
| `standard` | Neutral/standard Swahili with no strong dialect markers |

### `review_status` (4 values)

| Value | Description |
|-------|-------------|
| `draft` | Initial creation, not yet reviewed |
| `reviewed` | Reviewed by at least one annotator |
| `validated` | Passed double annotation + adjudication + schema validation |
| `disputed` | Annotators disagreed and adjudication is pending or unresolved |

---

## Controlled Vocabularies

Full controlled vocabulary files are in `dataset/metadata/`:

- `crop_vocabulary.json` — 12 priority crops with Swahili, English, and scientific names
- `pest_disease_vocab.json` — ~150 pest/disease entries with names, scientific names, categories, and applicable crops
- `category_definitions.json` — 11 categories with descriptions, examples, and diagnostic cues