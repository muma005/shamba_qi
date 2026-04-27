import pandas as pd
import json
import os
from sklearn.model_selection import train_test_split

def compute_splits():
    input_path = "dataset/processed/shambaqa_v1_release.jsonl"
    output_dir = "dataset/processed"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    # Load data
    print("Loading dataset...")
    df = pd.read_json(input_path, lines=True)
    
    # Save full dataset as Parquet
    full_parquet_path = os.path.join(output_dir, "shambaqa_v1.0.parquet")
    df.to_parquet(full_parquet_path, index=False)
    print(f"Full dataset saved to {full_parquet_path}")

    # Split: 80/10/10 (Train / Dev / Test)
    # Stratify by crop to ensure representative samples in all splits
    print("Generating stratified splits (80/10/10)...")
    
    train_df, temp_df = train_test_split(
        df, test_size=0.20, random_state=42, stratify=df['crop']
    )
    
    dev_df, test_df = train_test_split(
        temp_df, test_size=0.50, random_state=42, stratify=temp_df['crop']
    )

    # Save splits
    splits = {
        "train": train_df,
        "dev": dev_df,
        "test": test_df
    }

    for name, split_df in splits.items():
        path = os.path.join(output_dir, f"{name}.parquet")
        split_df.to_parquet(path, index=False)
        print(f"  - {name}: {len(split_df)} records saved to {path}")

    print("\nSplits computation complete.")

if __name__ == "__main__":
    compute_splits()
