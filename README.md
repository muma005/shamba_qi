# shamba_qi
# ShambaQA: Swahili Agricultural Pest & Disease Advisory QA Dataset

> **Zero Swahili agricultural QA datasets exist. This fills that gap.**

ShambaQA is an open-source question-answering dataset in Swahili (Kiswahili) covering crop pest and disease diagnostics for East African smallholder farmers. It pairs realistic farmer questions with authoritative expert answers sourced from agricultural extension materials.

---

## Quick Start

```python
from datasets import load_dataset

ds = load_dataset("username/shambaqa")
print(ds["train"][0])
```

---

## Key Statistics

| Metric | Value |
|--------|-------|
| Total QA pairs | *[UPDATE AFTER BUILD]* |
| Language | Swahili (Kiswahili) |
| Dialect variants | Kenyan Swahili, Tanzanian Swahili, Standard |
| Crops covered | 12 |
| Pest/disease entries | ~150 |
| Categories | 11 |
| Format | JSONL + CSV |
| Train / Dev / Test | 80% / 10% / 10% (stratified) |

---

## Scarcity Evidence

As of April 2026, searching HuggingFace for "Swahili agriculture", "Swahili pest", and "Kiswahili QA" returns zero matching datasets. Screenshots documenting this search are included in `docs/`.

*[INSERT SCREENSHOTS HERE]*

---

## Why This Dataset

33 million+ smallholder farmers in East Africa lose 30–40% of crops annually to pests and diseases (FAO). Digital advisory tools like iShamba and Plantwise are actively deploying SMS/WhatsApp-based farmer support but lack the NLP backbone for Swahili. ShambaQA provides the training and evaluation data to build that backbone.

---

## Target Users

- NLP researchers working on low-resource language QA
- Agritech startups building farmer advisory chatbots
- Agricultural extension organizations digitizing outreach
- Multilingual LLM evaluation teams needing domain-specific Swahili benchmarks

---

## Dataset Fields

See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for complete column definitions.

Key fields: `question_sw`, `answer_sw`, `crop`, `pest_disease`, `category`, `severity`, `source_ref`, `question_source`, `dialect_variant`, `confidence`

---

## Collection Methodology

Data was sourced from publicly available agricultural extension materials including KALRO pamphlets, FAO Swahili publications, Plantwise/CABI pest fact sheets, Shamba Shape Up TV transcripts, and agricultural radio call-in segments.

QA pairs were constructed using an LLM-assisted, human-reviewed pipeline. Questions follow four documented farmer communication patterns (symptom description, identification request, treatment request, prevention query). All answers are grounded in authoritative source material.

See [METHODOLOGY.md](METHODOLOGY.md) for the full collection and annotation methodology.

---

## Baselines

| Model | Task | Macro F1 |
|-------|------|----------|
| TF-IDF + Logistic Regression | Category classification | *[UPDATE]* |
| AfroXLMR-base (fine-tuned) | Category classification | *[UPDATE]* |

---

## Limitations

1. Questions are constructed from patterns, not sourced from real farmer conversations — may not capture the full messiness of real queries
2. Dialect representation is skewed toward Kenyan Swahili (~65%)
3. Text-only — no image-based diagnosis, which limits diagnostic accuracy
4. Severity labels involve subjective judgment and may not match clinical-grade plant pathology assessment
5. Answers are informational summaries, not professional agricultural extension advice

---

## Ethical Considerations

- No personally identifiable information in the dataset
- No banned pesticides (WHO Hazard Class Ia/Ib) recommended in any answer
- No commercial brand names — only generic active ingredients
- Risk of agricultural misinformation if models trained on this data are deployed without expert validation
- Any deployed system should include confidence scores and expert escalation paths

See [RESPONSIBLE_USE.md](RESPONSIBLE_USE.md) for deployment guidelines.

---

## Citation

```bibtex
@dataset{shambaqa2026,
  title={ShambaQA: Swahili Agricultural Pest & Disease Advisory QA Dataset},
  author={ShambaQA Contributors},
  year={2026},
  url={https://huggingface.co/datasets/username/shambaqa},
  license={CC-BY-SA-4.0}
}
```

---

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

---

## Acknowledgments

Data sourced from materials by KALRO (Kenya Agricultural and Livestock Research Organization), FAO (Food and Agriculture Organization of the United Nations), CABI (Centre for Agriculture and Bioscience International), and Mediae Company (Shamba Shape Up).