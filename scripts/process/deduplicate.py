import json
import os
import hashlib
from datetime import datetime

def get_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def deduplicate():
    input_path = "dataset/processed/shambaqa_validated.jsonl"
    output_path = "dataset/processed/shambaqa_v1_release.jsonl"
    report_path = "docs/deduplication_report.md"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f]
    
    total_start = len(records)
    unique_records = []
    seen_hashes = set()
    removed_count = 0

    for r in records:
        # Create a stable ID based on both Q and A
        # This preserves the 4-5 augmented patterns per segment
        composite_key = f"{r['question_sw']}|{r['answer_sw']}"
        h = get_hash(composite_key)
        
        if h not in seen_hashes:
            seen_hashes.add(h)
            r["review_status"] = "validated"
            unique_records.append(r)
        else:
            removed_count += 1

    # Save release version
    with open(output_path, "w", encoding="utf-8") as f:
        for r in unique_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # Generate Report
    report = f"""# Deduplication Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

- **Total Starting Records**: {total_start}
- **Total Duplicates Removed**: {removed_count}
- **Total Unique Records Remaining**: {len(unique_records)}
- **Deduplication Logic**: Composite MD5 (Question + Answer)
- **Status**: {"[PASS]" if len(unique_records) >= 1500 else "[STRETCH COLLECTION TRIGGERED]"}
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"Deduplication complete. {len(unique_records)} unique records remain.")
    return len(unique_records)

if __name__ == "__main__":
    deduplicate()
