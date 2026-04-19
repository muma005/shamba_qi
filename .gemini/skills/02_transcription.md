# 02 Transcription
Instructions for transcribing audio/video agricultural content.
# Skill 02 — Audio/Video Transcription

Use this when transcribing Shamba Shape Up episodes and agricultural radio segments.

---

## Sources

**Shamba Shape Up** (Primary)
- Kenyan agricultural TV show — YouTube channel (Mediae Company)
- Target: "Crop Doctor" segments where farmer describes symptoms, expert diagnoses/advises
- Expected: 200–400 QA pairs from 15–20 episodes
- Language: Swahili with some English code-switching

**Agricultural Radio** (Secondary)
- KBC and Radio Citizen farmer call-in shows
- Expected: 100–200 QA pairs from 10–15 segments
- Challenge: lower audio quality, overlapping speakers

---

## Episode Selection

Prioritize episodes featuring crop pest/disease content. Search titles for: "wadudu" (pests), "magonjwa" (diseases), "mahindi" (maize), "nyanya" (tomatoes), etc. Skip episodes focused on livestock, aquaculture, or market access.

Document for each episode: ID, title, date, relevant timestamp ranges.

---

## Transcription Pipeline

1. **Download**: yt-dlp to extract audio as WAV
2. **Transcribe**: Whisper large-v3 (or faster-whisper for speed) with `language="sw"` forced — do not let Whisper auto-detect
3. **Filter silence**: Skip segments with `no_speech_prob > 0.5`
4. **Correct ag terms**: Apply corrections dictionary for common Whisper errors on Swahili agricultural vocabulary
5. **Tag speakers**: Use content indicators (see below)
6. **Extract Q&A pairs**: Identify natural farmer question → expert answer exchanges

---

## Common Whisper Errors on Ag Terms

| Whisper Output | Correct Term |
|----------------|-------------|
| fungaside | fungicide |
| pestiside | pesticide |
| blaiti | blight |
| matone ya kahawia | madoa ya kahawia (brown spots) |

Expand this dictionary as you encounter new errors during correction passes.

---

## Speaker Role Tagging

Don't use a full diarization model. Use content indicators instead:

**Farmer indicators**: "shamba yangu" (my farm), "mimea yangu" (my plants), "nimepanda" (I planted), "nimeona" (I have seen), "tatizo langu" (my problem), "sielewi" (I don't understand)

**Expert indicators**: "ugonjwa huu" (this disease), "dawa ya" (medicine for), "suluhisho" (solution), "pendekezo" (recommendation), "kuzuia" (to prevent), "kutibu" (to treat), "ni muhimu" (it is important)

Tag each segment as `farmer`, `expert`, or `unknown` (flag for manual review).

---

## Q&A Extraction from Transcripts

From tagged transcripts, identify natural Q&A exchanges where:
- A farmer describes a crop symptom, pest observation, or agricultural problem
- An expert responds with diagnosis, treatment, or prevention advice

These are `direct_from_source` pairs — the highest quality type. Prioritize them.

**Rules:**
- Preserve original Swahili — do NOT translate or correct grammar
- Skip greetings, introductions, ad breaks, livestock segments, market discussion
- If an exchange spans multiple turns, merge the farmer's turns and the expert's turns
- One Q&A pair = one problem + one response — split multi-problem exchanges
- Remove speaker names, replace with role tags [Farmer], [Expert]

---

## Output

Each transcribed Q&A segment → JSONL with: segment_id, source_file, source_ref (e.g., "Shamba Shape Up S14E03, 12:30–14:15"), source_type (`radio_transcript`), farmer_text, expert_text, crop_detected, pest_disease_detected, start_time, end_time, transcription_confidence, question_source (`direct_from_source`), language, needs_manual_review, extracted_date

---

## Dependencies

System: `ffmpeg`
Python: `faster-whisper` (or `openai-whisper`), `yt-dlp`, `soundfile`

---

## Failure Modes

| Failure | Detection | Fix |
|---------|-----------|-----|
| Whisper detects wrong language | `language_detected != "sw"` | Force `language="sw"` |
| Music/jingles transcribed | High `no_speech_prob` | Filter segments > 0.5 |
| Speaker overlap | Repeated words, nonsense | Flag for manual review, extract only clean segments |
| English code-switching | Sudden language shift | Keep if agricultural term; split if full English sentence |
| Long episodes OOM | Whisper crashes | Split audio into 30-min chunks with 10s overlap |