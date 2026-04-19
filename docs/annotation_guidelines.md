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

**When in doubt between categories:** Choose the category that matches the ROOT CAUSE described in the answer, not the symptom the farmer describes. If the farmer thinks it's a disease but the expert identifies nutrient deficiency, label `nutrient_deficiency`.

---

## Label 3: Pest/Disease

Identify the specific pest or disease from the controlled vocabulary (`dataset/metadata/pest_disease_vocab.json`).

- Use the Swahili name as listed in the vocabulary
- If the pest/disease is not in the vocabulary, add it and note the addition
- If the answer discusses differential diagnosis (could be X or Y), label the first/most-likely one and reduce `confidence`

---

## Label 4: Severity

See [severity_rubric.md](severity_rubric.md) for the full rubric with examples.

**Critical rule:** Severity is based on the SCENARIO DESCRIBED in this specific QA pair, NOT the worst-case potential of the pest. A small early-stage Fall Armyworm sighting = `medium`. A full-blown Fall Armyworm outbreak destroying the field = `critical`.

---

## Label 5: Dialect Variant

| Value | Indicators |
|-------|-----------|
| `kenyan_swahili` | Kenya-specific terms, Kenyan farming context, references to Kenya locations/institutions |
| `tanzanian_swahili` | Tanzania-specific terms, Tanzanian farming context |
| `standard` | Neutral formal Swahili, no strong dialect markers |

---

## Label 6: Confidence

Rate your own confidence in the labels you assigned:

| Score | Meaning |
|-------|---------|
| 0.9–1.0 | Very confident — clear crop, clear pest, unambiguous severity |
| 0.7–0.89 | Confident — most labels clear, minor ambiguity on one |
| 0.5–0.69 | Moderate — some labels uncertain, could reasonably be labeled differently |
| Below 0.5 | Low — significant uncertainty, flag for adjudication |

---

## General Rules

1. **One primary crop per QA pair.** Do not list multiple crops.
2. **One primary pest/disease per QA pair.** If multiple are mentioned, label the primary one.
3. **Preserve the original text.** Do not modify `question_sw` or `answer_sw` during annotation. If you find errors, flag them in a comment — do not fix inline.
4. **When in doubt, flag.** Set confidence below 0.5 and add a note. It's better to flag than to guess.
5. **Refer to edge cases.** Check [edge_cases.md](edge_cases.md) if your situation isn't covered above.