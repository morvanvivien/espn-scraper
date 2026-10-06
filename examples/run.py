"""Minimal example: run the espn-scores-scraper Actor and print the results.

Usage: APIFY_TOKEN=... python run.py   (pip install apify-client)
"""
import os
import sys

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable first.")

client = ApifyClient(token)

run_input = {
    "league": "nfl",
    "mode": "results",
    "days": 14,
    "maxItems": 50,
}

run = client.actor("bibian/espn-scores-scraper").call(run_input=run_input)

count = 0
for item in client.dataset(run.default_dataset_id).iterate_items():
    count += 1
    print(f"{item['shortName']} | {item.get('awayScore')}-{item.get('homeScore')} | {item.get('statusDetail')}")
print(f"{count} results")
