# Changelog

All notable changes to ShambaQA will be documented in this file.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [1.0.0] — 2026-04-27

### Added
- Initial public release
- *[X,XXX]* QA pairs covering 12 crops and 11 categories
- Train/dev/test splits (80/10/10, stratified, no leakage)
- Controlled vocabularies: crops, pests/diseases, categories
- TF-IDF + Logistic Regression baseline
- AfroXLMR-base fine-tuning baseline
- Full documentation: README, DATA_DICTIONARY, METHODOLOGY, RESPONSIBLE_USE
- Demonstration notebook (`explore_dataset.ipynb`)
- CC BY-SA 4.0 license

---

## Planned

### [1.1.0]
- Expand to 5,000+ QA pairs
- Add livestock pest/disease coverage
- Increase Tanzanian Swahili representation

### [2.0.0]
- Community contribution pipeline with annotation guidelines
- Add Kikuyu and Luo translations
- Expand to 15+ crops