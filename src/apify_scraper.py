"""
Apify YouTube Scraper Module
Handles scraping YouTube channel videos using Apify's youtube-scraper actor
"""

import os
from apify_client import ApifyClient
from typing import List, Dict, Optional


class YouTubeScraper:
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize the YouTube scraper with Apify API token

        Args:
            api_token: Apify API token (defaults to APIFY_API_TOKEN env var)
        """
        self.api_token = api_token or os.getenv('APIFY_API_TOKEN')
        if not self.api_token:
            raise ValueError("Apify API token is required. Set APIFY_API_TOKEN environment variable.")

        self.client = ApifyClient(self.api_token)

    def scrape_channel(self, channel_url: str, max_videos: int = 50) -> List[Dict]:
        """
        Scrape videos from a YouTube channel

        Args:
            channel_url: URL of the YouTube channel
            max_videos: Maximum number of videos to scrape (default: 50)

        Returns:
            List of video dictionaries with title, url, description, and subtitles
        """
        print(f"🔍 Scraping YouTube channel: {channel_url}")
        print(f"📊 Fetching up to {max_videos} videos...")

        # Configure the actor run input
        run_input = {
            "startUrls": [{"url": channel_url}],
            "maxResults": max_videos,
            "subtitlesLanguage": "en",  # Get English subtitles
            "subtitlesFormat": "text",  # Get plain text format
        }

        # Run the actor and wait for it to finish
        print("⏳ Running Apify actor...")
        run = self.client.actor("streamers/youtube-scraper").call(run_input=run_input)

        # Fetch results from the actor's dataset
        videos = []
        print("📥 Fetching results...")

        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
            video_data = {
                'id': item.get('id', ''),
                'title': item.get('title', 'Untitled'),
                'url': item.get('url', ''),
                'description': item.get('description', ''),
                'date': item.get('date', ''),
                'subtitles': item.get('subtitles', ''),
                'views': item.get('viewCount', 0),
                'duration': item.get('duration', ''),
            }
            videos.append(video_data)

        # Sort videos by date (newest first)
        videos.sort(key=lambda x: x.get('date', ''), reverse=True)

        print(f"✅ Successfully scraped {len(videos)} videos!")
        return videos

    def get_video_transcript(self, video_url: str) -> Optional[str]:
        """
        Get transcript for a single video

        Args:
            video_url: URL of the YouTube video

        Returns:
            Video transcript as text
        """
        run_input = {
            "startUrls": [{"url": video_url}],
            "maxResults": 1,
            "subtitlesLanguage": "en",
            "subtitlesFormat": "text",
        }

        run = self.client.actor("streamers/youtube-scraper").call(run_input=run_input)

        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
            return item.get('subtitles', '')

        return None
