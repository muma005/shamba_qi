import os
import json
import uuid
from datetime import datetime

# Load Metadata
METADATA_DIR = "dataset/metadata"
EXTRACTED_DIR = "dataset/raw/extracted"
OUTPUT_PATH = "dataset/processed/shambaqa_final.jsonl"

with open(os.path.join(METADATA_DIR, "vocab_master.json"), "r", encoding="utf-8") as f:
    VOCAB = json.load(f)

CROP_VOCAB = VOCAB["crops"]

def generate_qa_patterns(segment):
    crop = segment["crop_sw"]
    raw_context = segment["raw_context"]
    # For now, we use the local common name if detected, else "pest"
    pest = segment.get("pest_disease_sw", "shida") 
    
    patterns = []
    
    # Pattern 1: Symptom-Based
    patterns.append({
        "question_sw": f"Majani yangu ya {crop} yanaonyesha dalili fulani, shida inaweza kuwa nini?",
        "answer_sw": raw_context,
        "pattern_type": "diagnostic"
    })
    
    # Pattern 2: Direct ID
    patterns.append({
        "question_sw": f"{pest} ni nini na inaadhiri vipi zao langu la {crop}?",
        "answer_sw": raw_context,
        "pattern_type": "direct_id"
    })
    
    # Pattern 3: Treatment
    patterns.append({
        "question_sw": f"Nifanye nini ili kudhibiti {pest} kwenye {crop} changu?",
        "answer_sw": raw_context,
        "pattern_type": "actionable"
    })
    
    return patterns

def main():
    os.makedirs("dataset/processed", exist_ok=True)
    
    # Load all atomic segments
    segments = []
    # ... (loading logic same as before)
    atomic_path = os.path.join(EXTRACTED_DIR, "atomic_segments.jsonl")
    if os.path.exists(atomic_path):
        with open(atomic_path, "r", encoding="utf-8") as f:
            for line in f:
                segments.append(json.loads(line))
    
    ssu_dir = os.path.join(EXTRACTED_DIR, "shamba_shape_up")
    if os.path.exists(ssu_dir):
        for f in os.listdir(ssu_dir):
            if f.endswith(".jsonl"):
                with open(os.path.join(ssu_dir, f), "r", encoding="utf-8") as f_in:
                    for line in f_in:
                        data = json.loads(line)
                        segments.append({
                            "source_ref": data["source_ref"],
                            "crop_sw": data["crop_detected"],
                            "raw_context": data["expert_text"],
                            "source_type": "transcript_segment"
                        })

    # Batch 2: Skip the first ~170 segments used in Batch 1
    OFFSET = 170 
    segments = segments[OFFSET:]
    
    # Counters for distribution
    crop_counts = {c: 0 for c in CROP_VOCAB.keys()}
    total_generated = 0
    
    # Append mode for Batch 2
    with open(OUTPUT_PATH, "a", encoding="utf-8") as f_out:
        for seg in segments:
            crop = seg.get("crop_sw", "unknown")
            if crop not in CROP_VOCAB: continue
            
            # Prioritize undersampled crops in this batch
            patterns = generate_qa_patterns(seg)
            
            for p in patterns:
                qa_pair = {
                    "id": str(uuid.uuid4()),
                    "question_sw": p["question_sw"],
                    "answer_sw": p["answer_sw"],
                    "question_en": None, 
                    "answer_en": None,
                    "crop": crop,
                    "pest_disease_scientific": "TBD",
                    "category": seg.get("category", "general_management"),
                    "severity": "medium",
                    "question_source": "constructed_from_pattern",
                    "dialect_variant": "standard"
                }
                f_out.write(json.dumps(qa_pair, ensure_ascii=False) + "\n")
                crop_counts[crop] += 1
                total_generated += 1
                
            if total_generated >= 500: break # Batch 2 target

    print(f"\nBatch 2 Execution Complete!")
    print(f"Total New QA Pairs Generated: {total_generated}")

if __name__ == "__main__":
    main()
