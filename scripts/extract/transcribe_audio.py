import os
import json
import torch
from faster_whisper import WhisperModel
from datetime import datetime

# Agricultural corrections dictionary from shamba.md
AGRI_CORRECTIONS = {
    "fungaside": "fungicide",
    "pestiside": "pesticide",
    "blaiti": "blight",
    "matone": "madoa",
    "insektisi": "insecticide",
    "bakteri": "bakteria",
    "nitrojin": "nitrojeni",
    "fosforasi": "fosforasi",
    "potasiam": "potasiamu",
    "vidukali": "vidukari"
}

# Speaker Detection Rules
FARMER_KEYWORDS = ["shamba yangu", "shamba langu", "mimea yangu", "nimepanda", "nimeona", "tatizo langu", "nisaidie", "nasaidia", "sielewi", "nifanye nini", "mahindi yangu", "nyanya zangu"]
EXPERT_KEYWORDS = ["ugonjwa huu", "ugonjwa huo", "dawa ya", "suluhisho", "pendekezo", "napendekeza", "hatua ya kwanza", "ni muhimu", "kuzuia", "kutibu", "udhibiti", "dalili", "chanzo"]
PRESENTER_KEYWORDS = ["karibu", "leo tutajifunza", "tunaendelea", "sehemu inayofuata"]

TRANSCRIPT_DIR = "dataset/raw/sources/shamba_shape_up/transcripts"
AUDIO_DIR = "dataset/raw/sources/shamba_shape_up"

def apply_corrections(text):
    for word, correction in AGRI_CORRECTIONS.items():
        text = text.replace(word, correction)
    return text

def detect_speaker(text):
    text_lower = text.lower()
    if any(k in text_lower for k in FARMER_KEYWORDS): return "farmer"
    if any(k in text_lower for k in EXPERT_KEYWORDS): return "expert"
    if any(k in text_lower for k in PRESENTER_KEYWORDS): return "presenter"
    return "unknown"

def transcribe_file(model, filename):
    audio_path = os.path.join(AUDIO_DIR, filename)
    video_id = os.path.splitext(filename)[0]
    
    print(f"Transcribing {filename}...")
    segments, info = model.transcribe(audio_path, language="sw", task="transcribe", word_timestamps=True)
    
    raw_segments = []
    total_segments = 0
    filtered_silence = 0
    
    for segment in segments:
        total_segments += 1
        if segment.no_speech_prob > 0.5:
            filtered_silence += 1
            continue
            
        seg_data = {
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip(),
            "avg_logprob": segment.avg_logprob,
            "no_speech_prob": segment.no_speech_prob,
            "speaker": detect_speaker(segment.text)
        }
        raw_segments.append(seg_data)

    # Save Raw
    raw_output = {
        "video_id": video_id,
        "source_file": filename,
        "language_forced": "sw",
        "total_segments": total_segments,
        "filtered_silence": filtered_silence,
        "segments": raw_segments,
        "full_text": " ".join([s["text"] for s in raw_segments])
    }
    
    raw_path = os.path.join(TRANSCRIPT_DIR, f"{video_id}_raw.json")
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw_output, f, indent=2, ensure_ascii=False)

    # Apply Corrections
    for seg in raw_segments:
        seg["text"] = apply_corrections(seg["text"])
    
    corrected_output = raw_output.copy()
    corrected_output["full_text"] = " ".join([s["text"] for s in raw_segments])
    
    corrected_path = os.path.join(TRANSCRIPT_DIR, f"{video_id}_corrected.json")
    with open(corrected_path, "w", encoding="utf-8") as f:
        json.dump(corrected_output, f, indent=2, ensure_ascii=False)
    
    print(f"Finished {video_id}. Extracted {len(raw_segments)} segments.")

def main():
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    
    print(f"Loading Whisper model on {device}...")
    model = WhisperModel("base", device=device, compute_type=compute_type)
    
    # Process one file for testing
    files = [f for f in os.listdir(AUDIO_DIR) if f.endswith((".webm", ".wav", ".m4a", ".mp3"))]
    if files:
        f = files[0]
        video_id = os.path.splitext(f)[0]
        if not os.path.exists(os.path.join(TRANSCRIPT_DIR, f"{video_id}_corrected.json")):
            transcribe_file(model, f)

if __name__ == "__main__":
    main()
