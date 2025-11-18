#!/usr/bin/env python3
"""
Debug script to inspect Apify YouTube scraper output
Shows all fields returned by the actor to help troubleshoot subtitle extraction
"""

import os
import sys
from dotenv import load_dotenv
from apify_client import ApifyClient
import json


def debug_apify_response(url: str):
    """
    Scrape a single URL and print all fields returned by Apify

    Args:
        url: YouTube URL to test
    """
    load_dotenv()

    api_token = os.getenv('APIFY_API_TOKEN')
    if not api_token:
        print("❌ Error: APIFY_API_TOKEN not found in environment")
        sys.exit(1)

    client = ApifyClient(api_token)

    print(f"🔍 Debugging Apify response for: {url}\n")
    print("=" * 70)

    # Configure the actor run input
    run_input = {
        "startUrls": [{"url": url}],
        "maxResults": 1,  # Just get one video for debugging
        "getSubtitles": True,  # Enable subtitle extraction
        "subtitlesLanguage": "en",
        "subtitlesFormat": "plaintext",
    }

    print("📤 Running Apify actor with input:")
    print(json.dumps(run_input, indent=2))
    print("\n⏳ Waiting for results...\n")

    # Run the actor
    run = client.actor("streamers/youtube-scraper").call(run_input=run_input)

    # Fetch and display results using list_items (best practice)
    print("=" * 70)
    print("📥 RESULTS:\n")

    dataset_client = client.dataset(run["defaultDatasetId"])
    dataset_items = dataset_client.list_items(limit=10)

    item_count = 0
    for item in dataset_items.items:
        item_count += 1
        print(f"--- Item {item_count} ---")
        print(f"Available fields: {list(item.keys())}\n")

        # Print all fields
        for key, value in item.items():
            if key == 'subtitles':
                # Show subtitles preview
                subtitle_preview = str(value)[:200] if value else "EMPTY or None"
                print(f"  {key}: {subtitle_preview}...")
                print(f"    -> Length: {len(str(value)) if value else 0} characters")
                print(f"    -> Type: {type(value)}")
                print(f"    -> Is empty: {not bool(value)}")
            elif isinstance(value, str) and len(str(value)) > 100:
                # Truncate long strings
                print(f"  {key}: {str(value)[:100]}... (length: {len(str(value))})")
            else:
                print(f"  {key}: {value}")

        print("\n" + "=" * 70)

        # Full JSON dump for inspection
        print("\n📋 Full JSON response:")
        print(json.dumps(item, indent=2, ensure_ascii=False)[:2000])
        print("\n...")

    if item_count == 0:
        print("⚠️  No items returned by the actor!")
        print("\nTroubleshooting:")
        print("  1. Check if the URL is valid")
        print("  2. Check if the video/channel has any videos")
        print("  3. Try a different URL")

    print("\n" + "=" * 70)
    print(f"✅ Debug complete! Total items: {item_count}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_apify.py <youtube_url>")
        print("\nExamples:")
        print("  python debug_apify.py 'https://www.youtube.com/watch?v=VIDEO_ID'")
        print("  python debug_apify.py 'https://www.youtube.com/@ChannelName'")
        sys.exit(1)

    url = sys.argv[1]
    debug_apify_response(url)
