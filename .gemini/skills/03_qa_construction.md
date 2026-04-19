# 03 QA Construction
Instructions for generating question-answer pairs from extracted text.
# Skill 03 — QA Pair Construction

Use this when converting extracted segments and transcripts into structured question-answer pairs.

---

## Approach: LLM-Assisted, Human-Reviewed

LLM generates draft QA pairs → human annotator reviews/corrects → validation script checks schema. The LLM does heavy lifting on question formulation; the human ensures agricultural accuracy and Swahili naturalness.

---

## Four Question Patterns

Every constructed question MUST fit one of these types:

### Type 1: Symptom Description

The farmer describes what they see on their crop.

Pattern: `[crop part] + [symptom observation] + [what is this?]`

- "Majani ya mahindi yangu yameanza kuwa na madoa ya kahawia, ni ugonjwa gani?"
- "Matunda ya nyanya yangu yana sehemu nyeusi chini, ni nini kinachosababisha?"
- "Mashina ya maharage yangu yameanza kunyauka ingawa ninamwagilia, tatizo ni nini?"

### Type 2: Direct Identification Request

The farmer asks to identify something they found.

Pattern: `[what is this?] + [description of pest/symptom]`

- "Hii ni nini? Nimepata wadudu wadogo weupe chini ya majani ya kahawa yangu."
- "Ni ugonjwa gani unaosababisha majani ya viazi kujikunja na kukauka?"

### Type 3: Treatment/Action Request

The farmer knows the problem, wants to know what to do.

Pattern: `[problem statement] + [what should I do?]`

- "Nifanye nini kuhusu funza wanaokula mahindi yangu shambani?"
- "Ninawezaje kutibu ugonjwa wa kutu kwenye ngano yangu?"

### Type 4: Prevention Query

The farmer asks how to prevent a problem.

Pattern: `[problem/pest] + [how to prevent?]`

- "Ninazuiaje wadudu wa kuhifadhi wasiharibu mahindi yangu baada ya kuvuna?"
- "Ni hatua gani za kuchukua kuzuia ugonjwa wa bacterial wilt kwenye nyanya?"

---

## Construction Rules

**For questions:**
- Write in natural Swahili as a real farmer would speak — not formal/academic
- Vary question patterns across pairs generated from the same segment
- Default dialect: Kenyan Swahili unless source is Tanzanian
- Each question must be specific enough that the answer is clearly grounded in the source

**For answers:**
- Must be factually grounded in the source segment — never add information not in the source
- Must be actionable — tell the farmer what to DO, not just what the problem IS
- Include both diagnosis AND management when the source provides both
- Keep technical terms if the source uses them
- Length: 2–5 sentences, concise but complete

**For metadata:**
- `question_source = "constructed_from_pattern"` for generated questions
- `question_source = "direct_from_source"` for questions from transcripts (highest quality — prioritize these)
- `question_source = "adapted_from_transcript"` for cleaned/restructured transcript exchanges

---

## LLM Prompt for Construction

When generating QA pairs from a segment, the LLM prompt should include:

1. The full segment text
2. The source reference
3. Detected crop and pest/disease
4. Instruction to generate 2–3 pairs with varied question patterns
5. The severity guidelines (see GEMINI.md)
6. The category enum list
7. Instruction to output JSON matching the schema
8. Explicit rule: "ONLY use information from the segment — do not hallucinate"

---

## For Direct-From-Source Pairs (Transcripts)

When the source is a Shamba Shape Up or radio transcript with a real farmer question:

- Preserve the farmer's original question as closely as possible — only fix obvious transcription errors
- Structure the expert's answer to be self-contained
- Do NOT rephrase the farmer's question into formal Swahili — keep it natural
- These demonstrate real farmer language patterns and are the most valuable entries

---

## Question Augmentation

When dataset size needs boosting from limited answer segments:

- Generate 2 alternative questions per existing answer (different patterns than original)
- Maximum 3 questions per unique answer (1 original + 2 augmented)
- Never augment answers — only questions
- Augmented pairs get `question_source = "constructed_from_pattern"`

---

## Distribution Monitoring

After every 500 pairs, check:

- No single crop > 25% of dataset — if so, force-sample other crops
- All 12 crops present — if any missing, actively seek source material
- All 11 categories present — if any has < 10 entries and total > 500, flag it
- Question pattern distribution — if any type > 60%, force rotation

---

## Failure Modes

| Failure | Detection | Fix |
|---------|-----------|-----|
| LLM generates overly formal Swahili | Questions sound like textbook | Add informal speech examples to prompt; specify "spoken, not written" |
| LLM hallucinates pest info | Answer has facts not in source | Cross-check against source_ref; add "ONLY source info" to prompt |
| All questions same pattern | Counter shows >60% one type | Force pattern rotation in prompt |
| English leaking into Swahili | Language detection < 0.9 | Flag sentences where >30% words are English |
| Duplicates across batches | Jaccard > 0.7 | Run dedup after every batch |
| Severity labels inconsistent | Same pest labeled differently | Create severity lookup table per pest |