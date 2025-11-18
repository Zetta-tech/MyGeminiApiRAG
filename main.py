#!/usr/bin/env python3
"""
YouTube Channel RAG - Main Application
Scrapes YouTube channel videos and enables chat with transcripts using Gemini AI
"""

import os
import sys
from dotenv import load_dotenv
from src.apify_scraper import YouTubeScraper
from src.gemini_client import GeminiRAG
from src.video_processor import VideoProcessor
from src.chat_interface import start_chat_session


def print_banner():
    """Print application banner"""
    print("\n" + "=" * 70)
    print("🎥 YouTube Channel RAG - Chat with Video Transcripts")
    print("=" * 70)
    print("\nPowered by Apify + Google Gemini AI")
    print()


def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['GEMINI_API_KEY', 'APIFY_API_TOKEN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"  • {var}")
        print("\nPlease create a .env file with the required variables.")
        print("See .env.example for reference.")
        sys.exit(1)


def get_channel_url():
    """Prompt user for YouTube channel URL"""
    print("📺 Enter the YouTube channel URL:")
    print("   Example: https://www.youtube.com/@channel_name")
    print("   Or: https://www.youtube.com/c/channel_name")
    print()

    while True:
        channel_url = input("Channel URL: ").strip()

        if not channel_url:
            print("⚠️  URL cannot be empty. Please try again.")
            continue

        if 'youtube.com' not in channel_url:
            print("⚠️  Please provide a valid YouTube URL.")
            continue

        return channel_url


def get_max_videos():
    """Prompt user for maximum number of videos to scrape"""
    print("\n📊 How many videos would you like to scrape?")
    print("   (Press Enter for default: 50)")
    print()

    while True:
        max_videos = input("Max videos [50]: ").strip()

        if not max_videos:
            return 50

        try:
            max_videos = int(max_videos)
            if max_videos <= 0:
                print("⚠️  Please enter a positive number.")
                continue
            return max_videos
        except ValueError:
            print("⚠️  Please enter a valid number.")
            continue


def main():
    """Main application function"""
    # Load environment variables
    load_dotenv()

    # Print banner
    print_banner()

    # Check environment variables
    check_environment()

    # Initialize clients
    print("🔧 Initializing clients...")
    youtube_scraper = YouTubeScraper()
    gemini_client = GeminiRAG()
    video_processor = VideoProcessor()
    print("✅ Clients initialized!\n")

    # Get user input
    channel_url = get_channel_url()
    max_videos = get_max_videos()

    print("\n" + "=" * 70)
    print("Starting process...")
    print("=" * 70)

    try:
        # Step 1: Scrape YouTube channel
        print("\n📥 STEP 1: Scraping YouTube Channel")
        print("-" * 70)
        videos = youtube_scraper.scrape_channel(channel_url, max_videos)

        if not videos:
            print("❌ No videos found. Please check the channel URL and try again.")
            sys.exit(1)

        # Step 2: Create transcript files
        print("\n📝 STEP 2: Creating Transcript Files")
        print("-" * 70)
        transcript_files = video_processor.create_all_transcript_files(videos)

        if not transcript_files:
            print("❌ No transcripts available. The videos may not have subtitles.")
            sys.exit(1)

        # Save metadata
        video_processor.save_metadata(videos)

        # Step 3: Upload files to Gemini
        print("\n☁️  STEP 3: Uploading Files to Gemini AI")
        print("-" * 70)
        gemini_client.upload_multiple_files(transcript_files)

        print("\n" + "=" * 70)
        print("✅ Setup Complete! Ready to chat!")
        print("=" * 70)

        # Step 4: Start chat interface
        print("\n💬 STEP 4: Starting Chat Interface")
        print("-" * 70)
        start_chat_session(gemini_client)

    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
