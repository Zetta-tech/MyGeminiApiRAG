# YouTube Channel RAG 🎥

A powerful tool that enables you to chat with YouTube video transcripts using Google's Gemini AI and Apify's YouTube scraper.

## Features

- 🔍 **Scrape YouTube Channels** - Automatically fetch videos from any YouTube channel
- 🚀 **Batch Processing** - Process multiple channels, playlists, or videos in parallel
- ⚡ **Async Support** - Lightning-fast parallel scraping using async/await
- 📝 **Extract Transcripts** - Get video subtitles and transcripts using Apify
- ☁️ **Gemini File Search** - Upload transcripts to Google's new Gemini file search feature
- 💬 **Interactive Chat** - Chat with your video transcripts using natural language
- 🎯 **Newest to Oldest** - Videos are automatically sorted from newest to oldest
- 📊 **Metadata Storage** - Save video metadata for future reference
- 📁 **File Input** - Load multiple URLs from a file for bulk processing

## Prerequisites

- Python 3.8 or higher
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Apify API token ([Get one here](https://console.apify.com/account/integrations))

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MyGeminiApiRAG
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   APIFY_API_TOKEN=your_apify_api_token_here
   ```

## Usage

### Quick Start (Single Channel)

Run the main application for a single channel:
```bash
python main.py
```

The application will:
1. Prompt you for a YouTube channel URL
2. Ask how many videos to scrape
3. Scrape the channel and extract transcripts
4. Upload transcripts to Gemini AI
5. Start an interactive chat interface

### Batch Processing (Multiple URLs)

For processing multiple channels, playlists, or videos in parallel:
```bash
python batch_main.py
```

The batch application supports three input modes:
1. **Manual Entry** - Enter URLs one by one interactively
2. **File Input** - Load URLs from a text file
3. **Single URL** - Process one channel/playlist

**Example: Using a URLs file**
```bash
# Create a file with your URLs (one per line)
cat > my_urls.txt << EOF
https://www.youtube.com/@Channel1
https://www.youtube.com/watch?v=VIDEO_ID
https://www.youtube.com/playlist?list=PLAYLIST_ID
EOF

# Run batch processing
python batch_main.py
# Select option 2 (Load URLs from file)
# Enter: my_urls.txt
```

**Benefits of Batch Processing:**
- ⚡ **Parallel Execution** - All URLs are scraped simultaneously
- 🚀 **Faster Processing** - Async/await for maximum performance
- 📊 **Better Organization** - All videos from multiple sources in one chat
- 🔄 **Reusable Tasks** - Option to create Apify tasks for repeated runs

### Example Session

```
🎥 YouTube Channel RAG - Chat with Video Transcripts
====================================================================

📺 Enter the YouTube channel URL:
Channel URL: https://www.youtube.com/@ExampleChannel

📊 How many videos would you like to scrape?
Max videos [50]: 20

🔍 Scraping YouTube channel...
✅ Successfully scraped 20 videos!

📝 Creating transcript files for 20 videos...
✅ Created 18 transcript files!

☁️ Uploading Files to Gemini AI...
✅ All files uploaded!

💬 You: What topics are covered in these videos?
🤖 Assistant: Based on the transcripts, the main topics include...
```

### Chat Commands

While in the chat interface, you can use:

- **Your question** - Ask anything about the video transcripts
- `help` or `?` - Show help message with example questions
- `list` - List all uploaded transcript files
- `clear` - Clear conversation history
- `exit` or `quit` - Exit the chat

### Example Questions to Ask

- "What topics are covered in these videos?"
- "Summarize the main points from [video title]"
- "What did they say about [specific topic]?"
- "Which video talks about [subject]?"
- "Create a summary of all the videos"
- "What are the key takeaways?"
- "Compare how different videos approach [topic]"

## Project Structure

```
MyGeminiApiRAG/
├── src/
│   ├── __init__.py
│   ├── apify_scraper.py      # Single URL YouTube scraping
│   ├── batch_scraper.py      # Batch scraping with async support
│   ├── gemini_client.py      # Gemini API with file search
│   ├── video_processor.py    # Video transcript processing
│   └── chat_interface.py     # Interactive chat interface
├── data/
│   └── transcripts/          # Stored video transcripts
├── main.py                   # Single channel application
├── batch_main.py             # Batch processing application
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── urls.txt.example          # Example URLs file for batch processing
└── README.md                 # This file
```

## How It Works

1. **YouTube Scraping**
   - Uses Apify's `streamers/youtube-scraper` actor
   - Fetches video metadata and English subtitles
   - **Batch Mode**: Processes multiple URLs in parallel using async/await
   - **Single Mode**: Processes one channel at a time
   - Sorts videos from newest to oldest

2. **Transcript Processing**
   - Creates individual text files for each video
   - Includes title, URL, description, and full transcript
   - Saves metadata in JSON format
   - Handles videos without subtitles gracefully

3. **Gemini File Search**
   - Uploads transcript files to Gemini API
   - Uses Google's new file search feature
   - Enables semantic search across all videos
   - Supports querying multiple video sources simultaneously

4. **Interactive Chat**
   - Natural language interface
   - Queries across all uploaded transcripts
   - Provides context-aware responses
   - Works seamlessly with single or batch-processed videos

## Advanced Features

### Async Batch Processing

The batch scraper implements Apify's best practices for handling multiple inputs:

**Standard Batch Mode** (Quick & Simple)
```python
from src.batch_scraper import scrape_urls_async
import asyncio

urls = [
    "https://www.youtube.com/@Channel1",
    "https://www.youtube.com/watch?v=VIDEO_ID",
    "https://www.youtube.com/playlist?list=PLAYLIST_ID"
]

videos = asyncio.run(scrape_urls_async(urls, max_videos_per_source=50))
```

**Task-Based Mode** (Recommended for Reusable Inputs)
```python
# Use this when you plan to scrape the same URLs multiple times
videos = asyncio.run(scrape_urls_async(urls, max_videos_per_source=50, use_tasks=True))
```

**Performance Benefits:**
- All URLs are scraped in parallel using `asyncio.gather()`
- Significantly faster than sequential processing
- Efficient resource utilization
- Automatic error handling for individual URLs

### URL File Format

Create a `urls.txt` file with one URL per line:
```
# Comments start with #
https://www.youtube.com/@TechChannel
https://www.youtube.com/watch?v=abc123
https://www.youtube.com/playlist?list=PLxxx

# Mix channels, playlists, and individual videos
https://www.youtube.com/@AnotherChannel
```

## API References

- **Gemini File Search**: [Documentation](https://ai.google.dev/gemini-api/docs/file-search)
- **Apify API**: [Documentation](https://docs.apify.com)
- **Apify Async Client**: [Best Practices](https://docs.apify.com/api/client/python/docs/async)
- **YouTube Scraper Actor**: [Documentation](https://apify.com/streamers/youtube-scraper)

## Troubleshooting

### No subtitles available
Some videos may not have subtitles. The tool will skip these videos automatically.

### API rate limits
- Apify has rate limits based on your plan
- Gemini API has upload and query limits
- Consider reducing the number of videos if you hit limits

### File upload errors
- Ensure your Gemini API key is valid
- Check that transcript files were created successfully
- Verify file sizes are within Gemini's limits

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project however you'd like!

## Acknowledgments

- [Google Gemini AI](https://ai.google.dev/) - For the powerful file search capabilities
- [Apify](https://apify.com/) - For the excellent YouTube scraper
- Built with ❤️ for the YouTube learning community