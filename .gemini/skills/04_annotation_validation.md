# 04 Annotation & Validation
Instructions for validating and annotating the ShambaQA dataset.
# Skill 04 — Annotation, Validation & Quality Control

Use this for labeling QA pairs, computing inter-annotator agreement, deduplication, and final validation.

---

## Annotation Workflow

```
Draft QA pairs (from Skill 03)
    ↓
Annotator A labels → Annotator B labels (independent)
    ↓
Automated agreement check
    ├── Agreement → Accept
    └── Disagreement → Adjudicator reviews
         ├── Clear error → Correct + log
         └── Legitimate ambiguity → Adjudicator decides + update edge case rules
    ↓
Schema validation script
    ↓
Language detection check
    ↓
Deduplication
    ↓
Domain expert spot-check (20% calibration phase, 10% rest)
    ↓
Final validated dataset
```

---

## Labels to Assign Per QA Pair

| Label | Type | Annotator Action |
|-------|------|-----------------|
| `crop` | Categorical (12 + "other") | Verify or correct crop identification |
| `category` | Categorical (11 values) | Classify pest/disease category |
| `pest_disease` | Controlled text (~150 entries) | Identify specific pest/disease |
| `severity` | Ordinal (4 levels) | Assess urgency from the scenario described |
| `dialect_variant` | Categorical (3 values) | Tag dialect from vocabulary/phrasing |
| `confidence` | Float 0–1 | Rate own certainty |

---

## Severity Rubric

| Level | Yield Impact | Spread | Example |
|-------|-------------|--------|---------|
| **low** | <5% | None | Minor leaf spots (cosmetic), small weed presence |
| **medium** | 5–20% | Localized | Early blight on a few plants, moderate aphid colony |
| **high** | 20–50% | Spreading | Stalk borer in multiple plants, late blight spreading |
| **critical** | >50% | Epidemic risk | Fall armyworm outbreak, bacterial wilt in irrigated field |

**Key rule**: Severity is based on the SCENARIO DESCRIBED, not the worst-case potential. A small, caught-early Fall Armyworm infestation = `medium`, not `critical`.

---

## Edge Case Rules

| Situation | Decision |
|-----------|----------|
| Question describes multiple problems | Split into separate QA pairs |
| Answer says "consult an expert" without diagnosis | `category = general_management`, `severity = high` |
| Nutrient deficiency mimicking disease symptoms | `category = nutrient_deficiency` (even if farmer assumes disease) |
| Post-harvest storage pest | Include, `category = storage_pest` |
| Question too vague for diagnosis | Include with `confidence < 0.5`, answer should request clarification |
| Pest could be multiple species | Label most likely, note uncertainty in `confidence` |
| Same answer covers multiple crops | One pair per crop, adjust answer per crop |
| Mixed Swahili/English answer | Acceptable if English terms are standard ag usage (fungicide, NPK) |
| Farmer uses slang/non-standard | Preserve as-is, tag `dialect_variant` accordingly |

---

## Inter-Annotator Agreement (IAA)

### Targets

| Label | Metric | Threshold |
|-------|--------|-----------|
| `crop` | Cohen's κ | ≥ 0.90 |
| `category` | Cohen's κ | ≥ 0.80 |
| `severity` | Weighted κ (quadratic) | ≥ 0.70 |
| `pest_disease` | Cohen's κ | ≥ 0.75 |

### Calibration Protocol

1. Select 200 QA pairs from Batch 1
2. Annotator A and B independently label all 200
3. Compute κ for each label
4. If ANY metric fails → identify disagreement patterns → revise guidelines → re-train → re-annotate fresh 100 pairs → re-compute
5. **GATE 2: Do NOT proceed to full annotation until all thresholds are met.**

---

## Schema Validation

`validate_schema.py` must check every record for:

- All non-nullable fields populated (see GEMINI.md schema table)
- All enum fields contain valid values
- `question_sw` length > 10 chars
- `answer_sw` length > 30 chars
- `confidence` in range 0.0–1.0
- `id` starts with `shambaqa-`
- Swahili language detection score > 0.9 on `question_sw` and `answer_sw` (fasttext `lid.176.bin`)
- `crop` value in controlled vocabulary (warn for "other")

Records that fail → `dataset/rejected/` with the error reason attached.

---

## Deduplication

- Tokenize all questions: lowercase + remove punctuation + whitespace split
- Compute pairwise Jaccard similarity
- Pairs with similarity > 0.7: keep higher confidence, discard the other
- Pairs with similarity 0.5–0.7: flag for manual review
- Run dedup after every batch, not just at the end

---

## Domain Expert Review

- **Calibration phase** (first 500 entries): 20% reviewed by agricultural domain expert
- **Remainder**: 10% spot-check
- Domain expert = someone with agricultural extension or plant pathology background
- Output: accuracy report per batch, systematic error flags

---

## Failure Modes

| Failure | Detection | Fix |
|---------|-----------|-----|
| IAA below threshold on severity | κ < 0.70 | Add concrete per-pest examples to rubric |
| Annotator labels crop from answer, not question | Inconsistency | Rule: question crop > answer crop > "general" |
| pest_disease granularity inconsistent | Mix of species and common names | Define target: species if identifiable, genus if not, common name if no Latin |
| Swahili detection false negatives | Agricultural English terms flag as English | Exclude known ag terms from detection input |