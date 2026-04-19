import os
import json
from datetime import datetime

TRANSCRIPT_DIR = "dataset/raw/sources/shamba_shape_up/transcripts"
EXTRACTED_DIR = "dataset/raw/extracted/shamba_shape_up"

CROP_KEYWORDS = {
    "mahindi": ["mahindi", "maize", "corn"],
    "nyanya": ["nyanya", "tomato"],
    "viazi": ["viazi", "potato"],
    "maharage": ["maharage", "beans"],
    "kahawa": ["kahawa", "coffee"],
    "ndizi": ["ndizi", "banana"],
    "mihogo": ["mihogo", "cassava"],
    "mpunga": ["mpunga", "rice"]
}

def detect_crop(text):
    text_lower = text.lower()
    for crop, kws in CROP_KEYWORDS.items():
        if any(kw in text_lower for kw in kws):
            return crop
    return "unknown"

def extract_exchanges(video_id):
    corrected_path = os.path.join(TRANSCRIPT_DIR, f"{video_id}_corrected.json")
    if not os.path.exists(corrected_path): return 0
    
    with open(corrected_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    segments = data["segments"]
    
    # Step 4 logic: Resolve 'unknown' speakers if they are between clear roles
    for i in range(1, len(segments) - 1):
        if segments[i]["speaker"] == "unknown":
            if segments[i-1]["speaker"] == "farmer" and segments[i+1]["speaker"] == "farmer":
                segments[i]["speaker"] = "farmer"
            elif segments[i-1]["speaker"] == "expert" and segments[i+1]["speaker"] == "expert":
                segments[i]["speaker"] = "expert"

    exchanges = []
    current_exchange = {"farmer": [], "expert": [], "start": None, "end": None, "crop": None}
    
    for seg in segments:
        speaker = seg["speaker"]
        text = seg["text"]
        
        if speaker == "farmer":
            if current_exchange["expert"]:
                exchanges.append(current_exchange)
                current_exchange = {"farmer": [], "expert": [], "start": None, "end": None, "crop": None}
            if not current_exchange["start"]: current_exchange["start"] = seg["start"]
            current_exchange["farmer"].append(text)
            if not current_exchange["crop"]: current_exchange["crop"] = detect_crop(text)
        elif speaker == "expert" and current_exchange["farmer"]:
            current_expert = current_exchange["expert"]
            current_expert.append(text)
            current_exchange["end"] = seg["end"]
        elif speaker == "presenter" and current_exchange["farmer"] and current_exchange["expert"]:
            exchanges.append(current_exchange)
            current_exchange = {"farmer": [], "expert": [], "start": None, "end": None, "crop": None}

    if current_exchange["farmer"] and current_exchange["expert"]:
        exchanges.append(current_exchange)

    output_path = os.path.join(EXTRACTED_DIR, f"{video_id}_exchanges.jsonl")
    count = 0
    with open(output_path, "w", encoding="utf-8") as f:
        for ex in exchanges:
            farmer_full = " ".join(ex["farmer"])
            expert_full = " ".join(ex["expert"])
            if len(farmer_full) < 10 or len(expert_full) < 30: continue
            
            def fmt_time(s):
                if s is None: return "00:00"
                m, sec = divmod(int(s), 60)
                return f"{m:02d}:{sec:02d}"

            ex_data = {
                "segment_id": f"seg-ssu-{video_id}-{count:03d}",
                "source_file": f"{video_id}.wav",
                "source_ref": f"Shamba Shape Up {video_id}, {fmt_time(ex['start'])}-{fmt_time(ex['end'])}",
                "source_type": "radio_transcript",
                "farmer_text": farmer_full,
                "expert_text": expert_full,
                "crop_detected": ex["crop"] or "unknown",
                "transcription_confidence": 1.0,
                "question_source": "direct_from_source",
                "language": "sw",
                "needs_manual_review": ex["crop"] == "unknown",
                "extracted_date": datetime.now().strftime("%Y-%m-%d")
            }
            f.write(json.dumps(ex_data, ensure_ascii=False) + "\n")
            count += 1
    return count

def generate_report(stats):
    print("\n=== Shamba Shape Up Pipeline Report ===")
    print(f"\nEXTRACTION:")
    print(f"  Total Q&A exchanges extracted: {sum(stats.values())}")
    print(f"  By episode:")
    for vid, count in stats.items():
        print(f"    - {vid}: {count}")
    
    est_qa = sum(stats.values()) * 1.5 # 1 exchange ≈ 1.5 QA pairs
    print(f"\nEstimated QA pairs from Shamba Shape Up: {int(est_qa)}")

def main():
    os.makedirs(EXTRACTED_DIR, exist_ok=True)
    stats = {}
    for f in os.listdir(TRANSCRIPT_DIR):
        if f.endswith("_corrected.json"):
            video_id = f.replace("_corrected.json", "")
            count = extract_exchanges(video_id)
            stats[video_id] = count
    
    if stats:
        generate_report(stats)
    else:
        print("No transcripts found to process.")

if __name__ == "__main__":
    main()
