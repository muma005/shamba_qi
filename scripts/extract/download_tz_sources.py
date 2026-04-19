import os
import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin, urlparse
from catalog_source import log_source

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

def download_pdf(url, folder, filename):
    try:
        response = requests.get(url, headers=HEADERS, stream=True, timeout=30)
        response.raise_for_status()
        path = os.path.join(folder, filename)
        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except: return False

def scrape_mkulima_mbunifu_mags():
    print("\n--- Scraping Mkulima Mbunifu Majarida ---")
    url = "https://mkulimambunifu.org/majarida/"
    subfolder = "mkulima_mbunifu"
    folder_path = os.path.join("dataset", "raw", "sources", subfolder)
    count = 0
    try:
        res = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.find_all("a", href=True)
        for l in links:
            if l["href"].endswith(".pdf"):
                abs_url = urljoin(url, l["href"])
                fname = os.path.basename(abs_url)
                # Avoid redownloading or downloading administrative PDFs
                if any(x in fname.lower() for x in ["tor", "tenda", "advert"]): continue
                
                if download_pdf(abs_url, folder_path, fname):
                    print(f"Downloaded Mag: {fname}")
                    log_source(fname, abs_url, "sw", "extension_pamphlet", "success", subfolder)
                    count += 1
    except Exception as e: print(f"Error Mkulima Mags: {e}")
    return count

def scrape_organic_africa_sw():
    print("\n--- Scraping Organic Africa Swahili ---")
    url = "https://www.organic-africa.net/training-manual/swahili-training-materials.html"
    subfolder = "organic_africa"
    folder_path = os.path.join("dataset", "raw", "sources", subfolder)
    count = 0
    try:
        res = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.find_all("a", href=True)
        for l in links:
            if l["href"].endswith(".pdf"):
                abs_url = urljoin(url, l["href"])
                fname = os.path.basename(abs_url)
                if download_pdf(abs_url, folder_path, fname):
                    print(f"Downloaded FiBL: {fname}")
                    log_source(fname, abs_url, "sw", "extension_pamphlet", "success", subfolder)
                    count += 1
    except Exception as e: print(f"Error OA: {e}")
    return count

def main():
    print("=== ShambaQA Tanzanian Source Acquisition (Phase 2) ===")
    results = {}
    results["Mkulima Mags"] = scrape_mkulima_mbunifu_mags()
    results["Organic Africa"] = scrape_organic_africa_sw()
    
    # Static list of high-yield PDFs from new_sources.md
    kh_pdf = "http://www.kilimohai.org/fileadmin/02_documents/15_Training_Materials/Wadudu__Magonjwa_na_Magugu_-_Pest___Disease_Management.pdf"
    if download_pdf(kh_pdf, "dataset/raw/sources/kilimohai", "Wadudu_Magonjwa_na_Magugu.pdf"):
        results["KilimoHai"] = 1
        log_source("Wadudu_Magonjwa_na_Magugu.pdf", kh_pdf, "sw", "extension_pamphlet", "success", "kilimohai")
    else: results["KilimoHai"] = 0

    print("\n--- Summary Report ---")
    total_files = sum(results.values())
    for k, v in results.items(): print(f"{k}: {v} files")
    
    # Yield estimate: Majarida are magazines (high yield), manuals are also high yield.
    # 50 QA pairs per magazine (avg), 30 per manual.
    est_yield = (results["Mkulima Mags"] * 50) + (results["Organic Africa"] * 30) + (results.get("KilimoHai", 0) * 40)
    total_est = 290 + est_yield
    print(f"\nProjected Total: {total_est}")
    print(f"GATE 1: {'PASS' if total_est >= 1200 else 'NEEDS MORE DATA'}")

if __name__ == "__main__":
    main()
