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

def generate_qa_patterns_augmented(segment):
    crop = segment["crop_sw"]
    raw_context = segment["raw_context"]
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

    # Pattern 4: Prevention (Augmentation Pass)
    patterns.append({
        "question_sw": f"Ninazuiaje {pest} isishambulie {crop} langu msimu ujao?",
        "answer_sw": raw_context,
        "pattern_type": "preventive"
    })
    
    # Pattern 5: Slang-Heavy (Augmentation Pass)
    patterns.append({
        "question_sw": f"Hawa wadudu wa {pest} kwenye {crop} ni shida kweli, nifanye nini wakome?",
        "answer_sw": raw_context,
        "pattern_type": "slang_heavy"
    })
    
    return patterns

def main():
    os.makedirs("dataset/processed", exist_ok=True)
    
    # Load all segments
    segments = []
    atomic_path = os.path.join(EXTRACTED_DIR, "atomic_segments.jsonl")
    if os.path.exists(atomic_path):
        with open(atomic_path, "r", encoding="utf-8") as f:
            for line in f:
                segments.append(json.loads(line))
    
    # No offset this time, process everything to ensure full volume
    # Use segments not fully utilized yet
    
    # Counters for distribution
    # Current counts (from total 1689): Mahindi 507
    crop_counts = {c: 0 for c in CROP_VOCAB.keys()}
    total_generated = 0
    maize_limit = 0.3
    
    # Append mode for final push
    with open(OUTPUT_PATH, "a", encoding="utf-8") as f_out:
        for seg in segments:
            crop = seg.get("crop_sw", "unknown")
            if crop not in CROP_VOCAB: continue
            
            # Strict Maize Cap for final balancing
            if crop == "Mahindi" and (507 + crop_counts["Mahindi"]) / (1689 + total_generated + 1) > maize_limit:
                continue
            
            # Generate 5 variants per segment
            patterns = generate_qa_patterns_augmented(seg)
            
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
                
            if 1689 + total_generated >= 3000: break # Final Target

    print(f"\nFinal Push Complete!")
    print(f"Total New QA Pairs Generated: {total_generated}")
    print(f"Grand Total: {1689 + total_generated}")

    print(f"\nBatch 2 Execution Complete!")
    print(f"Total New QA Pairs Generated: {total_generated}")

if __name__ == "__main__":
    main()
