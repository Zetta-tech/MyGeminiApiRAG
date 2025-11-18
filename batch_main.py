#!/usr/bin/env python3
"""
YouTube Batch RAG - Process Multiple YouTube URLs in Parallel
Supports channels, playlists, and individual videos
"""

import os
import sys
import asyncio
from dotenv import load_dotenv
from src.batch_scraper import scrape_urls_async
from src.gemini_client import GeminiRAG
from src.video_processor import VideoProcessor
from src.chat_interface import start_chat_session


def print_banner():
    """Print application banner"""
    print("\n" + "=" * 70)
    print("🚀 YouTube Batch RAG - Process Multiple Videos in Parallel")
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


def read_urls_from_file(file_path: str) -> list:
    """
    Read YouTube URLs from a file (one URL per line)

    Args:
        file_path: Path to the file containing URLs

    Returns:
        List of URLs
    """
    try:
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return urls
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)


def get_input_mode():
    """Prompt user for input mode"""
    print("📝 How would you like to provide YouTube URLs?")
    print("   1. Enter URLs manually (one at a time)")
    print("   2. Load URLs from a file")
    print("   3. Single channel/playlist")
    print()

    while True:
        choice = input("Select mode [1-3]: ").strip()

        if choice in ['1', '2', '3']:
            return int(choice)

        print("⚠️  Please select 1, 2, or 3.")


def get_manual_urls():
    """Get URLs manually from user"""
    print("\n📺 Enter YouTube URLs (channels, playlists, or videos)")
    print("   Press Enter on empty line when done")
    print("   Examples:")
    print("     - https://www.youtube.com/@ChannelName")
    print("     - https://www.youtube.com/watch?v=VIDEO_ID")
    print("     - https://www.youtube.com/playlist?list=PLAYLIST_ID")
    print()

    urls = []
    while True:
        url = input(f"URL {len(urls) + 1} (or Enter to finish): ").strip()

        if not url:
            if urls:
                break
            else:
                print("⚠️  Please enter at least one URL.")
                continue

        if 'youtube.com' not in url and 'youtu.be' not in url:
            print("⚠️  Please provide a valid YouTube URL.")
            continue

        urls.append(url)
        print(f"  ✓ Added: {url}")

    return urls


def get_file_path():
    """Get file path from user"""
    print("\n📁 Enter the path to your URLs file:")
    print("   File should contain one URL per line")
    print("   Lines starting with # are ignored")
    print()

    while True:
        file_path = input("File path: ").strip()

        if not file_path:
            print("⚠️  Please enter a file path.")
            continue

        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {file_path}")
            print("   Please check the path and try again.")
            continue

        return file_path


def get_single_url():
    """Get a single channel/playlist URL"""
    print("\n📺 Enter the YouTube channel or playlist URL:")
    print("   Examples:")
    print("     - https://www.youtube.com/@ChannelName")
    print("     - https://www.youtube.com/c/ChannelName")
    print("     - https://www.youtube.com/playlist?list=PLAYLIST_ID")
    print()

    while True:
        url = input("URL: ").strip()

        if not url:
            print("⚠️  URL cannot be empty. Please try again.")
            continue

        if 'youtube.com' not in url and 'youtu.be' not in url:
            print("⚠️  Please provide a valid YouTube URL.")
            continue

        return [url]


def get_max_videos():
    """Prompt user for maximum number of videos per source"""
    print("\n📊 Maximum videos to scrape per URL?")
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


def get_use_tasks():
    """Ask if user wants to use Apify tasks (for reusable inputs)"""
    print("\n⚙️  Use Apify tasks for reusable inputs?")
    print("   Recommended if you plan to run the same URLs multiple times")
    print("   (y/n, default: n)")
    print()

    choice = input("Use tasks? [y/N]: ").strip().lower()
    return choice in ['y', 'yes']


async def main_async():
    """Main async application function"""
    # Load environment variables
    load_dotenv()

    # Print banner
    print_banner()

    # Check environment variables
    check_environment()

    # Initialize clients
    print("🔧 Initializing clients...")
    gemini_client = GeminiRAG()
    video_processor = VideoProcessor()
    print("✅ Clients initialized!\n")

    # Get input mode
    input_mode = get_input_mode()

    # Get URLs based on input mode
    if input_mode == 1:
        urls = get_manual_urls()
    elif input_mode == 2:
        file_path = get_file_path()
        urls = read_urls_from_file(file_path)
        print(f"\n✅ Loaded {len(urls)} URL(s) from file")
    else:  # input_mode == 3
        urls = get_single_url()

    if not urls:
        print("❌ No URLs provided. Exiting.")
        sys.exit(1)

    # Get configuration
    max_videos = get_max_videos()
    use_tasks = get_use_tasks()

    print("\n" + "=" * 70)
    print("Starting batch processing...")
    print(f"URLs: {len(urls)}")
    print(f"Max videos per URL: {max_videos}")
    print(f"Using Apify tasks: {'Yes' if use_tasks else 'No'}")
    print("=" * 70)

    try:
        # Step 1: Scrape all URLs in parallel
        print("\n📥 STEP 1: Scraping YouTube URLs in Parallel")
        print("-" * 70)

        videos = await scrape_urls_async(
            urls,
            max_videos_per_source=max_videos,
            use_tasks=use_tasks
        )

        if not videos:
            print("❌ No videos found. Please check the URLs and try again.")
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


def main():
    """Entry point that runs the async main function"""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
