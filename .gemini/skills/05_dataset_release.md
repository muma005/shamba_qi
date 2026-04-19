# 05 Dataset Release
Instructions for final processing and releasing the dataset versions.
# Skill 05 — Dataset Release & Competition Submission

Use this for the final phase: splits, baselines, documentation, repo structure, HuggingFace upload, and submission.

---

## Train/Dev/Test Splits

- **Ratio**: 80% train / 10% dev / 10% test
- **Method**: Stratified by `crop` AND `category`
- **Seed**: 42 (non-negotiable)
- **Leakage prevention**: QA pairs sharing the same `answer_sw` must ALL be in the same split. If you augmented questions (multiple questions → same answer), those pairs stay together.

After splitting, verify:
- Split counts sum to full dataset count
- No answer text appears in more than one split
- Distributions are roughly similar across splits

---

## Baselines

### Baseline 1: TF-IDF + Logistic Regression

- **Task**: Category classification from `question_sw`
- **Config**: max_features=5000, ngram_range=(1,2), sublinear_tf=True, class_weight="balanced"
- **Expected Macro F1**: 0.45–0.55
- If > 0.60: task may be too easy (categories too keyword-separable)
- If < 0.40: check for labeling errors
- Output: classification report + confusion matrix PNG

### Baseline 2: AfroXLMR-base

- **Model**: `Davlan/afro-xlmr-base`
- **Config**: 5 epochs, batch_size=16, lr=2e-5, seed=42
- **Expected Macro F1**: 0.65–0.75
- Output: best checkpoint, classification report, learning curve plot

### Baseline 3: LLM Zero-Shot (Optional)

- GPT-4o and/or Claude Sonnet on 200-sample test subset
- Structured prompt with category definitions
- Expected Macro F1: 0.50–0.68

### Learning Curve

Train TF-IDF+LogReg on 10%, 20%, 30%, 50%, 70%, 100% of training data. Plot Macro F1 vs fraction. This proves the dataset has value even at smaller sizes.

---

## Documentation

### README.md Must Include

1. One-paragraph overview + "Zero Swahili ag QA datasets exist" headline
2. Quick start: 3-line code snippet to load via HuggingFace `datasets`
3. Key statistics table (total pairs, language, crops, format)
4. HuggingFace search screenshots showing zero existing datasets (scarcity proof)
5. Dataset fields summary (link to DATA_DICTIONARY.md)
6. Collection methodology summary (link to METHODOLOGY.md)
7. Baseline results table
8. Limitations (5 items — constructed questions, dialect skew, text-only, severity subjectivity, informational only)
9. Ethical considerations summary (link to RESPONSIBLE_USE.md)
10. BibTeX citation block
11. License: CC BY-SA 4.0

### DATA_DICTIONARY.md

All 20 columns: name, type, description, example value, nullable, controlled vocabulary list where applicable.

### METHODOLOGY.md

Source inventory, extraction procedures per source type, QA pair construction protocol, translation methodology, sampling strategy, deduplication algorithm. Be extremely precise — this is what makes the dataset reproducible.

### RESPONSIBLE_USE.md

- Minimum confidence thresholds for deployment
- Mandatory expert review for `critical` severity predictions
- User-facing uncertainty communication requirements
- Explicit statement: not a substitute for professional agricultural extension advice

---

## Repository Checklist

Before pushing to GitHub, verify:

- All files match the directory structure in GEMINI.md
- No absolute paths in any script
- `.gitignore` excludes: `__pycache__`, `.venv`, `*.wav`/`*.mp3`/`*.mp4`, `lid.176.bin`, model checkpoints
- `requirements.txt` has pinned versions
- `CITATION.cff` is valid CFF format
- `LICENSE` is CC BY-SA 4.0 full text

---

## HuggingFace Upload

1. `huggingface-cli login`
2. `huggingface-cli repo create shambaqa --type dataset`
3. Upload `dataset/processed/` contents + README.md as dataset card
4. Verify: `datasets.load_dataset("username/shambaqa")` works and shows correct schema

---

## Final Smoke Test (smoke_test.sh)

This runs BEFORE submission. Every check must pass:

1. All required files exist (README, METHODOLOGY, DATA_DICTIONARY, RESPONSIBLE_USE, CITATION.cff, LICENSE, all processed data, all metadata JSONs, all docs, example scripts, key scripts)
2. `validate_schema.py` passes on 100% of records
3. Split counts match full dataset count
4. No answer leakage between splits
5. TF-IDF baseline runs and reports Macro F1
6. `load_dataset.py` example runs
7. `explore_dataset.ipynb` executes end-to-end

**GATE 4: Nothing ships until smoke test passes.**

---

## Failure Modes

| Failure | Detection | Fix |
|---------|-----------|-----|
| Stratified split fails | sklearn ValueError | Merge rare strata or use simple random for rare classes |
| HuggingFace rejects format | Upload error | Verify JSONL: one object per line, no trailing commas, UTF-8 |
| Notebook fails on fresh machine | Import/path error | Relative paths, pin all deps, no hardcoded absolutes |
| Baseline F1 = 0.0 for some classes | Classification report | Verify min 10 samples per class in test split |
| README doesn't render | Broken formatting | Test with `grip` locally or push to test repo first |