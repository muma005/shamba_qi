# Responsible Use
Guidelines for ethical use and deployment of models trained on ShambaQA.
# ShambaQA Responsible Use Guidelines

This document provides guidelines for responsible deployment of models trained on ShambaQA.

---

## Intended Uses

- Training and evaluating Swahili QA models for agricultural advisory
- Benchmarking multilingual LLMs on domain-specific Swahili tasks
- Research on low-resource language NLP
- Prototyping farmer advisory chatbots with human expert oversight

---

## Out-of-Scope Uses

- **Automated agricultural advice without human expert oversight.** No model trained on this dataset should provide recommendations to farmers without a qualified agricultural extension officer in the loop.
- **Commercial pesticide recommendation systems.** The dataset contains generic active ingredient references, not product-specific recommendations. It is not suitable for driving purchasing decisions.
- **Replacing professional plant pathology diagnosis.** Text-based diagnosis has inherent limitations. Image-based and field-based assessment remain necessary for accurate identification.
- **Evaluating or ranking traditional farming knowledge.** The dataset reflects formal extension service perspectives. It should not be used to judge indigenous or community-specific agricultural practices.

---

## Deployment Requirements

Any system deployed to real farmers using models trained on ShambaQA must meet these minimum requirements:

### 1. Confidence Thresholds

- Do not present answers to users when model confidence is below 0.6
- For `severity = critical` predictions, require model confidence above 0.8 before presenting
- When confidence is below threshold, route to a human expert

### 2. Expert Escalation

- Every deployed system must include an escalation path to a qualified agricultural extension officer
- Users must be able to reach a human within the same interaction flow
- `severity = critical` predictions should trigger automatic expert notification

### 3. Uncertainty Communication

- Always communicate uncertainty to the end user
- Suggested framing: "Hii inaweza kuwa..." (This could be...) rather than "Hii ni..." (This is...)
- Never present model outputs as definitive diagnosis

### 4. Pesticide Safety

- Never recommend pesticides classified as WHO Hazard Class Ia (extremely hazardous) or Ib (highly hazardous)
- Always include safety precautions when recommending any pesticide application
- Prefer integrated pest management (IPM) recommendations over chemical-only solutions

### 5. Feedback Loop

- Deployed systems should collect user feedback on answer quality
- Incorrect answers should be logged for dataset improvement
- Do not collect personally identifiable information in feedback

---

## Known Risks

| Risk | Description | Mitigation |
|------|-------------|-----------|
| Misdiagnosis | Model predicts wrong pest/disease, farmer applies wrong treatment | Confidence thresholds + expert escalation |
| Severity underestimation | Model labels `critical` problem as `low`, farmer delays action | Conservative severity calibration + expert review for all critical cases |
| Dialect bias | Model performs worse on Tanzanian Swahili due to training skew | Monitor per-dialect performance, expand Tanzanian coverage in v2 |
| Outdated information | Pest management recommendations change over time | Version the dataset, encourage periodic retraining |
| Access inequality | Dataset benefits organizations with ML capacity, not directly farmers | Open-source license + deployment guidelines encourage broad access |

---

## Reporting Issues

If you identify errors, harmful content, or ethical concerns in the dataset, please open an issue on the GitHub repository or contact *[INSERT CONTACT]*.