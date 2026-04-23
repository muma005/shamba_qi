import json
import os
import numpy as np

def generate_stats():
    release_path = "dataset/processed/shambaqa_v1_release.jsonl"
    if not os.path.exists(release_path): return

    records = []
    with open(release_path, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))

    total = len(records)
    
    crops = {}
    categories = {}
    severities = {}
    q_lengths = []
    a_lengths = []

    for r in records:
        crops[r["crop"]] = crops.get(r["crop"], 0) + 1
        categories[r["category"]] = categories.get(r["category"], 0) + 1
        severities[r["severity"]] = severities.get(r["severity"], 0) + 1
        q_lengths.append(len(r["question_sw"]))
        a_lengths.append(len(r["answer_sw"]))

    stats = {
        "total_pairs": total,
        "crop_distribution": crops,
        "category_distribution": categories,
        "severity_distribution": severities,
        "mean_question_length": int(np.mean(q_lengths)),
        "mean_answer_length": int(np.mean(a_lengths)),
        "median_answer_length": int(np.median(a_lengths)),
        "status": "RELEASE_READY"
    }

    with open("dataset/metadata/dataset_statistics.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    
    print(f"Dataset Statistics Generated.")
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    generate_stats()
