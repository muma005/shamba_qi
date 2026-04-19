import os
import subprocess
import json
from datetime import datetime
from catalog_source import log_source

TIER_1_IDS = [
    "byVKUAg0Wb4", "PUYNaTtpulo", "2IGU-VEwI9Y", "kWy4ezP2qzA", 
    "cjaRdCcJwzw", "_vcAnxB0QmY", "f2FIQY2f5k8"
]

PODCAST_EPISODES = [
    {"title": "Crop Pests", "url": "https://shambashapeup.com/podcast/crop-pests/"},
    {"title": "Crop Diseases", "url": "https://shambashapeup.com/podcast/crop-diseases/"},
    {"title": "Harvesting & Storage", "url": "https://shambashapeup.com/podcast/harvesting-storage/"}
]

SUBFOLDER = "shamba_shape_up"
FOLDER_PATH = os.path.join("dataset", "raw", "sources", SUBFOLDER)
MANIFEST_PATH = os.path.join(FOLDER_PATH, "manifest.jsonl")

def get_video_info(video_id):
    cmd = ["python", "-m", "yt_dlp", "--get-title", "--get-duration", f"https://www.youtube.com/watch?v={video_id}"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")
        title = lines[0]
        duration_str = lines[1]
        # Convert duration to seconds
        parts = list(map(int, duration_str.split(':')))
        duration = parts[0] * 60 + parts[1] if len(parts) == 2 else parts[0] * 3600 + parts[1] * 60 + parts[2]
        return title, duration
    except:
        return f"Unknown Title ({video_id})", 0

def download_youtube_audio(video_id, tier):
    title, duration = get_video_info(video_id)
    lang = "sw" if "swa" in title.lower() or "swahili" in title.lower() else "en"
    
    print(f"Downloading {video_id} ({title})...")
    # Download best audio only, let yt-dlp decide the format (.m4a, .webm, etc)
    cmd = [
        "python", "-m", "yt_dlp", "-f", "bestaudio/best",
        "-o", os.path.join(FOLDER_PATH, "%(id)s.%(ext)s"),
        f"https://www.youtube.com/watch?v={video_id}"
    ]
    
    status = "success"
    filename = None
    try:
        subprocess.run(cmd, check=True)
        # Find what extension was actually used
        for ext in ['m4a', 'webm', 'wav', 'mp3']:
            test_path = os.path.join(FOLDER_PATH, f"{video_id}.{ext}")
            if os.path.exists(test_path):
                filename = f"{video_id}.{ext}"
                break
        
        if filename:
            log_source(filename, f"https://youtube.com/watch?v={video_id}", lang, "radio_transcript", "success", SUBFOLDER)
        else:
            status = "failed"
    except:
        status = "failed"
        print(f"Failed to download {video_id}")

    manifest_entry = {
        "video_id": video_id,
        "title": title,
        "tier": tier,
        "language_downloaded": lang,
        "filename": filename if status == "success" else None,
        "duration_seconds": duration,
        "download_status": status,
        "download_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    with open(MANIFEST_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(manifest_entry) + "\n")

def main():
    os.makedirs(FOLDER_PATH, exist_ok=True)
    for vid_id in TIER_1_IDS:
        download_youtube_audio(vid_id, 1)
    
    # Podcast logic - manual for now as per shamba.md instruction if automation fails
    for pod in PODCAST_EPISODES:
        log_source(None, pod["url"], "sw", "radio_transcript", "MANUAL_REQUIRED", SUBFOLDER, f"Podcast: {pod['title']}")

if __name__ == "__main__":
    main()
