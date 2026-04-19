import json
import hashlib
import os
from datetime import datetime

INVENTORY_PATH = os.path.join("dataset", "raw", "sources", "source_inventory.jsonl")

def get_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def log_source(filename, url, language, source_type, download_status="success", subfolder=None, notes=""):
    access_date = datetime.now().strftime("%Y-%m-%d")
    sha256 = None
    file_size_bytes = None
    
    if download_status == "success" and filename:
        file_path = os.path.join("dataset", "raw", "sources", subfolder if subfolder else "", filename)
        if os.path.exists(file_path):
            sha256 = get_sha256(file_path)
            file_size_bytes = os.path.getsize(file_path)
        else:
            download_status = "error"
            notes = f"File not found after download: {file_path}. " + notes

    entry = {
        "filename": filename,
        "url": url,
        "access_date": access_date,
        "sha256": sha256,
        "file_size_bytes": file_size_bytes,
        "language": language,
        "source_type": source_type,
        "download_status": download_status,
        "subfolder": subfolder,
        "notes": notes
    }
    
    with open(INVENTORY_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    # Example usage / manual entry
    import argparse
    parser = argparse.ArgumentParser(description="Log a source to the inventory.")
    parser.add_argument("--filename", help="Name of the file")
    parser.add_argument("--url", required=True, help="Source URL")
    parser.add_argument("--language", required=True, help="sw/en/mixed")
    parser.add_argument("--source_type", required=True, help="Type of source")
    parser.add_argument("--status", default="success", help="download_status")
    parser.add_argument("--subfolder", help="Subfolder in dataset/raw/sources/")
    parser.add_argument("--notes", default="", help="Additional notes")
    
    args = parser.parse_args()
    log_source(args.filename, args.url, args.language, args.source_type, args.status, args.subfolder, args.notes)
