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
    # This is a heuristic pass, real classification happens via LLM/Expert
    text_lower = text.lower()
    mapping = {
        "fungi": "fungal_disease", "fangasi": "fungal_disease",
        "bacteria": "bacterial_disease", "bakteria": "bacterial_disease",
        "virus": "viral_disease",
        "wadudu": "insect_pest", "pest": "insect_pest",
        "insect": "insect_pest", "funza": "insect_pest",
        "weed": "weed", "magugu": "weed"
    }
    for kw, cat in mapping.items():
        if kw in text_lower:
            return cat
    return "general_management"

def process_pdf(file_path, subfolder):
    filename = os.path.basename(file_path)
    print(f"Processing: {filename}...")
    doc = fitz.open(file_path)
    segments = []
    
    for page_num, page in enumerate(doc):
        text = page.get_text("text")
        
        # Simple atomic split by paragraph for now, 
        # to be refined by advisory logic
        paragraphs = text.split("\n\n")
        
        for para in paragraphs:
            para = para.strip()
            if len(para) < 50: continue # Skip fragments
            
            crop = detect_crop(para)
            if not crop: continue # Guardrail: DISCARD if no priority crop
            
            category = detect_category(para)
            
            segment = {
                "source_ref": f"{filename} (Page {page_num+1})",
                "crop_sw": crop,
                "pest_disease_sw": "unknown", # To be refined in construction
                "category": category,
                "raw_context": para,
                "segment_type": "constructed_from_text",
                "speaker_role": None,
                "extraction_quality_score": 0.9 # Default for native text
            }
            segments.append(segment)
            
    doc.close()
    return segments

def main():
    os.makedirs(EXTRACTED_DIR, exist_ok=True)
    all_segments = []
    
    # Process KALRO and Mkulima Mbunifu subfolders
    for sub in ["kalro", "mkulima_mbunifu"]:
        sub_path = os.path.join(SOURCE_DIR, sub)
        if not os.path.exists(sub_path): continue
        
        for f in os.listdir(sub_path):
            if f.endswith(".pdf"):
                path = os.path.join(sub_path, f)
                try:
                    results = process_pdf(path, sub)
                    all_segments.extend(results)
                except Exception as e:
                    print(f"Failed to process {f}: {e}")
                    
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
            
    print(f"\nExtraction Complete!")
    print(f"Total Unique Segments: {len(unique_segments)}")
    
    # Report count per crop
    crop_stats = {}
    for s in unique_segments:
        c = s["crop_sw"]
        crop_stats[c] = crop_stats.get(c, 0) + 1
    
    print("\nSegments per Crop:")
    for crop, count in crop_stats.items():
        print(f"  {crop}: {count}")

if __name__ == "__main__":
    main()
