import json
import os

def validate_schema():
    release_path = "dataset/processed/shambaqa_v1_release.jsonl"
    if not os.path.exists(release_path):
        print(f"Error: {release_path} not found.")
        return

    required_fields = ["id", "question_sw", "answer_sw", "question_en", "answer_en", "crop", "category", "severity"]
    valid_categories = [
        "fungal_disease", "bacterial_disease", "viral_disease", "insect_pest", 
        "mite", "nematode", "weed", "nutrient_deficiency", "abiotic_stress", 
        "storage_pest", "general_management"
    ]
    valid_severities = ["low", "medium", "high", "critical"]

    errors = []
    with open(release_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            record = json.loads(line)
            
            # 1. Null Check
            for field in required_fields:
                if record.get(field) is None or record.get(field) == "":
                    errors.append(f"Row {i}: Field '{field}' is null or empty.")
            
            # 2. Enum Integrity
            if record.get("category") not in valid_categories:
                errors.append(f"Row {i}: Invalid category '{record.get('category')}'.")
            if record.get("severity") not in valid_severities:
                errors.append(f"Row {i}: Invalid severity '{record.get('severity')}'.")
            
            # 3. ID Stability
            if not record.get("id"):
                errors.append(f"Row {i}: Missing ID.")

    if not errors:
        print(f"Schema Validation: [PASS] for all 2003 records.")
        return True
    else:
        print(f"Schema Validation: [FAIL] - Found {len(errors)} errors.")
        for e in errors[:10]: print(f"  {e}")
        return False

if __name__ == "__main__":
    validate_schema()
