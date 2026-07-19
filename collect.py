import requests
import json
import csv
import time

BASE_URL = "https://arbeitnow.com/api/job-board-api"

all_offers = []
current_url = BASE_URL
page_number = 1

# loop through all pages until there is no "next" link
while current_url:
    print(f"Fetching page {page_number}...")

    try:
        response = requests.get(current_url, timeout=10)
        response.raise_for_status()  # raises an error if status_code is 4xx or 5xx
    except requests.exceptions.Timeout:
        print("Request timed out. Skipping this page.")
        break
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        break
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
        break

    payload = response.json()
    job_offers = payload["data"]
    all_offers.extend(job_offers)

    current_url = payload["links"]["next"]
    page_number += 1

    time.sleep(1)  # wait 1 second between requests

print(f"Total number of job offers collected: {len(all_offers)}")

# build a cleaned list with only the useful fields
cleaned_offers = []

for offer in all_offers:
    cleaned_offer = {
        "title": offer["title"],
        "company": offer["company_name"],
        "location": offer["location"],
        "remote": offer["remote"],
        "job_types": offer["job_types"],
        "tags": offer["tags"],
        "created_at": offer["created_at"],
        "url": offer["url"]
    }
    cleaned_offers.append(cleaned_offer)

# save the cleaned data as JSON
with open("job_offers.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_offers, f, indent=2, ensure_ascii=False)

print("Data saved to job_offers.json")

# save the cleaned data as CSV
with open("job_offers.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=cleaned_offers[0].keys())
    writer.writeheader()
    for offer in cleaned_offers:
        offer_row = offer.copy()
        offer_row["job_types"] = ", ".join(offer["job_types"])
        offer_row["tags"] = ", ".join(offer["tags"])
        writer.writerow(offer_row)

print("Data saved to job_offers.csv")