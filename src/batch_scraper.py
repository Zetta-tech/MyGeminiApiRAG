"""
Batch YouTube Scraper Module with Async Support
Handles scraping multiple YouTube videos in parallel using Apify's async client
"""

import os
import asyncio
from apify_client import ApifyClientAsync
from typing import List, Dict, Optional


class BatchYouTubeScraper:
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize the batch YouTube scraper with Apify API token

        Args:
            api_token: Apify API token (defaults to APIFY_API_TOKEN env var)
        """
        self.api_token = api_token or os.getenv('APIFY_API_TOKEN')
        if not self.api_token:
            raise ValueError("Apify API token is required. Set APIFY_API_TOKEN environment variable.")

        self.client = ApifyClientAsync(self.api_token)

    async def scrape_multiple_urls(
        self,
        urls: List[str],
        max_videos_per_source: int = 50
    ) -> List[Dict]:
        """
        Scrape multiple YouTube URLs in parallel (channels, playlists, or individual videos)

        Args:
            urls: List of YouTube URLs (channels, playlists, or videos)
            max_videos_per_source: Maximum videos to scrape per URL (default: 50)

        Returns:
            List of video dictionaries with title, url, description, and subtitles
        """
        print(f"\n🚀 Starting batch scraping of {len(urls)} URL(s) in parallel...")

        # Run all scraping tasks in parallel
        tasks = [
            self._scrape_single_url(url, max_videos_per_source)
            for url in urls
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Flatten results and filter out errors
        all_videos = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"⚠️  Error scraping URL {i+1}: {result}")
                continue
            all_videos.extend(result)

        # Sort all videos by date (newest first)
        all_videos.sort(key=lambda x: x.get('date', ''), reverse=True)

        print(f"\n✅ Batch scraping complete! Total videos: {len(all_videos)}")
        return all_videos

    async def _scrape_single_url(
        self,
        url: str,
        max_videos: int = 50
    ) -> List[Dict]:
        """
        Scrape a single YouTube URL

        Args:
            url: YouTube URL (channel, playlist, or video)
            max_videos: Maximum number of videos to scrape

        Returns:
            List of video dictionaries
        """
        print(f"🔍 Scraping: {url}")

        # Configure the actor run input
        run_input = {
            "startUrls": [{"url": url}],
            "maxResults": max_videos,
            "getSubtitles": True,  # Enable subtitle extraction
            "subtitlesLanguage": "en",
            "subtitlesFormat": "plaintext",
        }

        try:
            # Run the actor and wait for it to finish
            run = await self.client.actor("streamers/youtube-scraper").call(run_input=run_input)

            # Fetch results from the actor's dataset using list_items (best practice)
            dataset_client = self.client.dataset(run["defaultDatasetId"])
            dataset_items = await dataset_client.list_items(limit=max_videos)

            # Process dataset items
            videos = []
            for idx, item in enumerate(dataset_items.items):
                # Debug: Show available fields for first item
                if idx == 0:
                    print(f"    🔍 Debug - Available fields: {list(item.keys())}")
                    subtitles_value = item.get('subtitles', '')
                    print(f"    🔍 Debug - Subtitles type: {type(subtitles_value)}, "
                          f"length: {len(str(subtitles_value)) if subtitles_value else 0}")

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

            print(f"  ✓ Scraped {len(videos)} video(s) from {url}")
            return videos

        except Exception as e:
            print(f"  ✗ Error scraping {url}: {e}")
            raise

    async def scrape_with_tasks(
        self,
        urls: List[str],
        max_videos_per_source: int = 50
    ) -> List[Dict]:
        """
        Scrape multiple URLs using Apify tasks for reusable inputs (best practice)

        Args:
            urls: List of YouTube URLs
            max_videos_per_source: Maximum videos per URL

        Returns:
            List of video dictionaries
        """
        print(f"\n🚀 Creating {len(urls)} Apify tasks for batch processing...")

        # Create Apify tasks
        apify_tasks = []
        apify_tasks_client = self.client.tasks()

        for i, url in enumerate(urls):
            task_name = f'youtube-scraper-{i}-{url.split("/")[-1][:20]}'
            try:
                apify_task = await apify_tasks_client.create(
                    name=task_name,
                    actor_id='streamers/youtube-scraper',
                    task_input={
                        "startUrls": [{"url": url}],
                        "maxResults": max_videos_per_source,
                        "getSubtitles": True,  # Enable subtitle extraction
                        "subtitlesLanguage": "en",
                        "subtitlesFormat": "plaintext",
                    },
                    memory_mbytes=1024,
                )
                apify_tasks.append(apify_task)
                print(f"  ✓ Created task: {task_name}")
            except Exception as e:
                print(f"  ✗ Error creating task for {url}: {e}")
                continue

        if not apify_tasks:
            print("❌ No tasks created successfully")
            return []

        print(f"\n⏳ Executing {len(apify_tasks)} tasks in parallel...")

        # Create task clients
        apify_task_clients = []
        for apify_task in apify_tasks:
            task_id = apify_task['id']
            apify_task_client = self.client.task(task_id)
            apify_task_clients.append(apify_task_client)

        # Execute tasks in parallel
        run_apify_tasks = [self._run_task(client) for client in apify_task_clients]
        task_run_results = await asyncio.gather(*run_apify_tasks, return_exceptions=True)

        # Process results
        all_videos = []
        for i, result in enumerate(task_run_results):
            if isinstance(result, Exception):
                print(f"  ✗ Task {i+1} failed: {result}")
                continue

            videos = result.get('videos', [])
            all_videos.extend(videos)
            print(f"  ✓ Task {i+1} completed: {len(videos)} video(s)")

        # Clean up tasks
        print(f"\n🗑️  Cleaning up {len(apify_tasks)} tasks...")
        for apify_task in apify_tasks:
            try:
                await apify_tasks_client.delete(apify_task['id'])
            except Exception as e:
                print(f"  ⚠️  Error deleting task: {e}")

        # Sort all videos by date
        all_videos.sort(key=lambda x: x.get('date', ''), reverse=True)

        print(f"\n✅ Batch processing complete! Total videos: {len(all_videos)}")
        return all_videos

    async def _run_task(self, task_client) -> Dict:
        """
        Run a single Apify task

        Args:
            task_client: Apify task client

        Returns:
            Dictionary with videos
        """
        try:
            run = await task_client.call()

            # Fetch videos from dataset using list_items (best practice)
            dataset_client = self.client.dataset(run["defaultDatasetId"])
            dataset_items = await dataset_client.list_items(limit=1000)

            # Process dataset items
            videos = []
            for idx, item in enumerate(dataset_items.items):
                # Debug: Show available fields for first item
                if idx == 0:
                    print(f"    🔍 Debug - Available fields: {list(item.keys())}")
                    subtitles_value = item.get('subtitles', '')
                    print(f"    🔍 Debug - Subtitles type: {type(subtitles_value)}, "
                          f"length: {len(str(subtitles_value)) if subtitles_value else 0}")

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

            return {'videos': videos}

        except Exception as e:
            raise Exception(f"Task execution failed: {e}")

    async def close(self):
        """Close the async client"""
        # ApifyClientAsync doesn't require explicit closing in current version
        pass


async def scrape_urls_async(
    urls: List[str],
    max_videos_per_source: int = 50,
    use_tasks: bool = False
) -> List[Dict]:
    """
    Convenience function to scrape multiple URLs asynchronously

    Args:
        urls: List of YouTube URLs
        max_videos_per_source: Maximum videos per URL
        use_tasks: Use Apify tasks for reusable inputs (recommended for repeated scraping)

    Returns:
        List of video dictionaries
    """
    scraper = BatchYouTubeScraper()

    try:
        if use_tasks:
            videos = await scraper.scrape_with_tasks(urls, max_videos_per_source)
        else:
            videos = await scraper.scrape_multiple_urls(urls, max_videos_per_source)

        return videos
    finally:
        await scraper.close()
