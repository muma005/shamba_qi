# Severity Rubric
Definitions for rating the severity of agricultural pests, diseases, and nutritional deficiencies.
# ShambaQA Severity Rubric

Use this rubric when assigning severity labels. Severity is based on the SCENARIO DESCRIBED, not the worst-case potential of the pest.

---

## Severity Levels

### LOW — Minor/Cosmetic Damage

**Definition:** Less than 5% expected yield loss. No active spread. Non-urgent.

**Examples:**
- A few leaves on one maize plant have small brown spots, rest of field is healthy
- Minor cosmetic blemishes on tomato fruit skin
- Small patch of weeds at field edge, not yet competing with crop
- Slight yellowing of lower/older leaves (normal aging, not deficiency)
- A handful of aphids on one bean plant

**Farmer action:** Monitor. No immediate intervention needed.

---

### MEDIUM — Moderate Damage

**Definition:** 5–20% expected yield loss. Localized spread. Action needed within days to weeks.

**Examples:**
- Early blight on several tomato plants, contained to one section
- Moderate aphid colony on beans — honeydew visible but plants still growing
- Small Fall Armyworm presence caught early — a few plants affected
- Mild nitrogen deficiency showing across part of the maize field
- Powdery mildew appearing on lower leaves of several plants
- Storage weevil found in a few maize cobs after harvest

**Farmer action:** Treat soon. Apply recommended management before spread worsens.

---

### HIGH — Significant Damage

**Definition:** 20–50% expected yield loss. Actively spreading. Action needed this week.

**Examples:**
- Late blight spreading across potato field — multiple plants showing symptoms daily
- Stalk borers boring into maize stems across several rows
- Severe nitrogen deficiency — most of the field shows yellowing and stunted growth
- Coffee berry disease affecting fruit on multiple branches across several trees
- Striga emerging in sorghum field — purple flowers visible between rows
- Larger grain borer found throughout stored maize — significant powder accumulation

**Farmer action:** Act now. Apply treatment, remove affected plants, seek extension advice.

---

### CRITICAL — Severe/Epidemic Risk

**Definition:** More than 50% expected yield loss. Epidemic potential. May affect neighboring farms. Action needed today.

**Examples:**
- Fall Armyworm outbreak — heavy infestation across the entire maize field
- Bacterial wilt in irrigated tomato field — multiple plants wilting daily, spreading through water
- Cassava Mosaic Disease with >50% plants showing severe leaf distortion
- Maize Streak Virus spreading rapidly through leafhopper vectors
- Quarantine pest detected (e.g., a pest requiring official notification)
- Total post-harvest grain loss — weevils have destroyed most of the stored harvest

**Farmer action:** Emergency. Seek expert help immediately. May need to notify agricultural authorities for quarantine pests.

---

## Common Pitfalls

| Mistake | Correction |
|---------|-----------|
| Labeling Fall Armyworm as always `critical` | Severity depends on the infestation level described, not the pest identity |
| Labeling nutrient deficiency as `low` because it's "not a disease" | Severe nutrient deficiency can cause 50%+ yield loss — assess based on impact described |
| Labeling any answer that says "consult an expert" as `critical` | Expert referral happens at all severity levels. Assess the underlying problem. |
| Labeling based on the crop value rather than the damage described | A problem on coffee isn't automatically more severe than one on maize. Judge the scenario. |

---

## When You're Unsure

- If the scenario sits between two levels, choose the HIGHER one and set confidence to 0.6–0.7
- If the text doesn't describe enough detail to assess severity, set `severity = medium` as the baseline and set confidence below 0.5
- If two annotators disagree on severity by more than one level (e.g., one says `low`, other says `high`), the pair goes to adjudication