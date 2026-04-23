# Annotation Guidelines
Detailed instructions for human annotators to ensure consistency in QA pairs.
# ShambaQA Annotation Guidelines

These guidelines govern how QA pairs are labeled. Read this document fully before beginning annotation.

---

## Your Task

For each QA pair, you will verify or assign the following labels:

1. **crop** — Which crop is this about?
2. **category** — What type of problem is described?
3. **pest_disease** — What specific pest or disease is identified?
4. **severity** — How urgent is this problem?
5. **dialect_variant** — Which Swahili dialect is used?
6. **confidence** — How confident are you in your labels?

---

## Label 1: Crop

Identify the primary crop referenced in the QA pair.

**Decision rule:**
1. If the question names a crop → use that crop
2. If the question is crop-generic but the answer names a crop → use the answer's crop
3. If both are truly generic → label `general`

Use the Swahili name from the controlled vocabulary: mahindi, maharage, mpunga, ngano, viazi, nyanya, vitunguu, kahawa, chai, ndizi, mihogo, mtama.

If the crop is not in the 12 priority crops, label `other`.

---

## Label 2: Category

Classify the pest/disease/problem into exactly one of these 11 categories:

| Category | Use When... |
|----------|-------------|
| `fungal_disease` | Caused by fungi — spots with rings, powdery coating, rust pustules, fungal wilting |
| `bacterial_disease` | Caused by bacteria — water-soaked lesions, bacterial ooze, foul-smelling rot |
| `viral_disease` | Caused by viruses — mosaic patterns, leaf curling, stunting, color breaking |
| `insect_pest` | Damage from insects — chewing marks, bore holes, visible insects, frass |
| `mite` | Fine webbing, stippling/bronzing, tiny dots on leaf underside |
| `nematode` | Root galling, stunted growth without foliar cause, patchy field pattern |
| `weed` | Crop competition, parasitic weeds (Striga, dodder) |
| `nutrient_deficiency` | Uniform yellowing (N), purpling (P), edge scorching (K), interveinal chlorosis (Fe/Zn) |
| `abiotic_stress` | Drought, waterlogging, frost, heat, chemical injury — non-living cause |
| `storage_pest` | Post-harvest: holes in grain, powder in bags, weevils |
| `general_management` | No specific pest — crop rotation, soil prep, IPM overview, seed selection |

---

## Label 3: Pest/Disease

Identify the specific pest or disease from the controlled vocabulary (`dataset/metadata/pest_disease_vocab.json`).

- Use the Swahili name as listed in the vocabulary
- If the answer discusses differential diagnosis (could be X or Y), label the first/most-likely one and reduce `confidence`

---

## Label 4: Severity

See the Severity Rubric below for levels.

**Critical rule:** Severity is based on the SCENARIO DESCRIBED in this specific QA pair, NOT the worst-case potential of the pest.

---

## Label 5: Dialect Variant

| Value | Indicators |
|-------|-----------|
| `kenyan_swahili` | Kenya-specific terms, Kenyan farming context |
| `tanzanian_swahili` | Tanzania-specific terms, Tanzanian farming context |
| `standard` | Neutral formal Swahili, no strong dialect markers |

---

## Severity Rubric
Enforce the following levels strictly during adjudication:
* **Low**: Cosmetic damage, < 5% loss. No immediate threat to food security.
* **Medium**: 5–20% loss, localized. Requires standard integrated pest management (IPM).
* **High**: 20–50% loss, active spread. Immediate intervention required.
* **Critical**: > 50% loss or quarantine pests (e.g., Desert Locust, Maize Lethal Necrosis). Threat to livelihood/food security.

## Edge Case Resolution
* **Ambiguous Symptoms**: If symptoms could indicate multiple diseases, the answer must provide broad advice or request further clarification. Confidence scores should be < 0.8.
* **Dialect Handling**: 'kenyan_swahili' vs 'tanzanian_swahili' must be tagged based on regional terminology (e.g., "dawa ya kunyunyizia" is typical in Kenyan advisory).
* **Scientific Alignment**: Always cross-reference Swahili common names with the scientific names in `vocab_master.json`.

---

## General Rules

1. **One primary crop per QA pair.**
2. **One primary pest/disease per QA pair.**
3. **Preserve the original text.**
4. **When in doubt, flag.**
