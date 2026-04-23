import os
import json
import fitz  # PyMuPDF
import hashlib
from datetime import datetime

# Controlled Vocabulary from ph2.md
PRIORITY_CROPS = [
    "Mahindi", "Maharage", "Mpunga", "Ngano", "Viazi", "Nyanya", 
    "Vitunguu", "Kahawa", "Chai", "Ndizi", "Mihogo", "Mtama"
]

CATEGORIES = [
    "fungal_disease", "bacterial_disease", "viral_disease", "insect_pest", 
    "mite", "nematode", "weed", "nutrient_deficiency", "abiotic_stress", 
    "storage_pest", "general_management"
]

EXTRACTED_DIR = "dataset/raw/extracted"
SOURCE_DIR = "dataset/raw/sources"

def get_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def detect_crop(text):
    text_lower = text.lower()
    for crop in PRIORITY_CROPS:
        if crop.lower() in text_lower:
            return crop
    return None

def detect_category(text):
    text_lower = text.lower()
    mapping = {
        "fungi": "fungal_disease", "fangasi": "fungal_disease", "ukungu": "fungal_disease", "kutu": "fungal_disease",
        "bacteria": "bacterial_disease", "bakteria": "bacterial_disease", "mnyauko": "bacterial_disease",
        "virus": "viral_disease", "bakatua": "viral_disease",
        "wadudu": "insect_pest", "pest": "insect_pest", "insect": "insect_pest", "funza": "insect_pest", "vidukari": "insect_pest", "utitiri": "mite",
        "weed": "weed", "magugu": "weed"
    }
    for kw, cat in mapping.items():
        if kw in text_lower:
            return cat
    return "general_management"

def process_pdf(file_path):
    filename = os.path.basename(file_path)
    print(f"Processing PDF: {filename}...")
    try:
        doc = fitz.open(file_path)
        segments = []
        for page_num, page in enumerate(doc):
            text = page.get_text("text")
            paragraphs = text.split("\n\n")
            for para in paragraphs:
                para = para.strip()
                if len(para) < 50: continue
                crop = detect_crop(para)
                if not crop: continue
                segments.append({
                    "source_ref": f"{filename} (Page {page_num+1})",
                    "crop_sw": crop,
                    "pest_disease_sw": "unknown",
                    "category": detect_category(para),
                    "raw_context": para,
                    "segment_type": "constructed_from_text",
                    "speaker_role": None,
                    "extraction_quality_score": 0.9
                })
        doc.close()
        return segments
    except: return []

def process_json(file_path):
    filename = os.path.basename(file_path)
    print(f"Processing JSON: {filename}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        text = data.get("body_text", "")
        crop = detect_crop(text)
        if not crop: return []
        return [{
            "source_ref": data.get("url", filename),
            "crop_sw": crop,
            "pest_disease_sw": "unknown",
            "category": detect_category(text),
            "raw_context": text,
            "segment_type": "constructed_from_text",
            "speaker_role": None,
            "extraction_quality_score": 1.0
        }]
    except: return []

def main():
    os.makedirs(EXTRACTED_DIR, exist_ok=True)
    all_segments = []
    
    # Walk through ALL source folders
    for root, dirs, files in os.walk(SOURCE_DIR):
        for f in files:
            path = os.path.join(root, f)
            if f.endswith(".pdf"):
                all_segments.extend(process_pdf(path))
            elif f.endswith(".json") and "manifest" not in f:
                all_segments.extend(process_json(path))
                    
    # Dedup and save
    seen_hashes = set()
    unique_segments = []
    for s in all_segments:
        h = get_hash(s["raw_context"])
        if h not in seen_hashes:
            seen_hashes.add(h)
            unique_segments.append(s)
            
    output_path = os.path.join(EXTRACTED_DIR, "atomic_segments.jsonl")
    with open(output_path, "w", encoding="utf-8") as f:
        for s in unique_segments:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
            
    print(f"\nMaster Extraction Complete!")
    print(f"Total Unique Atomic Segments: {len(unique_segments)}")
    
    crop_stats = {}
    for s in unique_segments:
        c = s["crop_sw"]
        crop_stats[c] = crop_stats.get(c, 0) + 1
    
    print("\nSegments per Crop:")
    for crop, count in sorted(crop_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {crop}: {count}")

if __name__ == "__main__":
    main()
