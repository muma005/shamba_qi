# Source Inventory
Tracking of all PDF and audio sources used to construct the dataset.
# ShambaQA Source Inventory

This document logs all data sources used in ShambaQA. The machine-readable version with SHA256 hashes is in `dataset/raw/sources/source_inventory.jsonl`.

---

## Source Summary

| # | Source | Files | Status | Language | Est. Yield |
|---|--------|-------|--------|----------|-----------|
| 1 | KALRO Extension Pamphlets | *[UPDATE]* | *[PENDING/ACCESSED/BLOCKED]* | SW & EN | 500–800 |
| 2 | FAO Swahili Publications | *[UPDATE]* | *[PENDING/ACCESSED/BLOCKED]* | SW | 300–500 |
| 3 | Plantwise/CABI Knowledge Bank | *[UPDATE]* | *[PENDING/ACCESSED/BLOCKED]* | EN | 400–600 |
| 4 | CABI Swahili Pest Guides | *[UPDATE]* | *[PENDING/ACCESSED/BLOCKED]* | SW | 200–300 |
| 5 | Shamba Shape Up Episodes | *[UPDATE]* | *[PENDING/ACCESSED/BLOCKED]* | SW | 200–400 |
| 6 | Agricultural Radio Segments | *[UPDATE]* | *[PENDING/ACCESSED/BLOCKED]* | SW | 100–200 |
| 7 | Extension Officer Training Manuals | *[UPDATE]* | *[PENDING/ACCESSED/BLOCKED]* | SW & EN | 200–300 |

**Total estimated yield:** 1,900–3,200 raw pairs → conservative 1,700 after filtering

---

## Detailed Source Log

### 1. KALRO Extension Pamphlets

- **URL:** https://www.kalro.org/publications
- **Access date:** *[UPDATE]*
- **Files downloaded:** *[LIST]*
- **Notes:** *[UPDATE]*

### 2. FAO Swahili Publications

- **URL:** https://www.fao.org/documents
- **Search terms used:** "Kiswahili", "farmer field school", "IPM", "pest management"
- **Access date:** *[UPDATE]*
- **Files downloaded:** *[LIST]*
- **Notes:** *[UPDATE]*

### 3. Plantwise/CABI Knowledge Bank

- **URL:** https://www.plantwise.org/knowledgebank
- **Access date:** *[UPDATE]*
- **Files downloaded:** *[LIST]*
- **Notes:** Mostly English. Swahili translations checked via CABI BioProtection Portal.

### 4. CABI Swahili Pest Guides

- **URL:** https://bioprotectionportal.com
- **Access date:** *[UPDATE]*
- **Files downloaded:** *[LIST]*
- **Notes:** *[UPDATE]*

### 5. Shamba Shape Up Episodes

- **URL:** YouTube — Mediae Company channel
- **Episodes selected:** *[LIST episode IDs, titles, relevant timestamps]*
- **Access date:** *[UPDATE]*
- **Selection criteria:** Episodes featuring crop pest/disease segments, "Crop Doctor" segments
- **Notes:** *[UPDATE]*

### 6. Agricultural Radio Segments

- **Stations:** KBC, Radio Citizen
- **Segments captured:** *[LIST]*
- **Access date:** *[UPDATE]*
- **Notes:** *[UPDATE]*

### 7. Extension Officer Training Manuals

- **Counties contacted:** *[LIST]*
- **Materials received:** *[LIST]*
- **Access date:** *[UPDATE]*
- **Notes:** *[UPDATE]*

---

## Blocked or Unavailable Sources

| Source | Reason | Fallback |
|--------|--------|----------|
| *[LIST ANY BLOCKED SOURCES]* | *[REASON]* | *[ALTERNATIVE]* |

---

## Wayback Machine Archives

Where possible, sources have been archived via the Internet Archive Wayback Machine to ensure long-term availability:

| Source | Wayback URL |
|--------|------------|
| *[UPDATE]* | *[UPDATE]* |

---

## GATE 1 Check

**Estimated total yield from accessible sources:** *[UPDATE]*

- [ ] ≥ 1,200 QA pairs estimated → **GATE 1 PASSED**
- [ ] < 1,200 QA pairs estimated → **GATE 1 FAILED — escalate and revise plan**