import json
import os
import time

import requests

from utils.extract import build_urls, parse_page

EXTRACTED_FILE = "extracted_data.json"


def run_extract(output_file: str = EXTRACTED_FILE, use_cache: bool = True, delay_seconds: float = 1.0):
    if use_cache and os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"File {output_file} found, data loaded from cache.")
        return data

    urls = build_urls()
    data = []

    for url in urls:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        products = parse_page(response.text)
        data.extend(products)

        print(f"Successfully scraped {url}")
        time.sleep(delay_seconds)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(data)} records to {output_file}")
    return data


def main():
    run_extract()


if __name__ == "__main__":
    main()