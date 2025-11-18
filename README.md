# YouTube Channel RAG 🎥

A powerful tool that enables you to chat with YouTube video transcripts using Google's Gemini AI and Apify's YouTube scraper.

## Features

- 🔍 **Scrape YouTube Channels** - Automatically fetch videos from any YouTube channel
- 📝 **Extract Transcripts** - Get video subtitles and transcripts using Apify
- ☁️ **Gemini File Search** - Upload transcripts to Google's new Gemini file search feature
- 💬 **Interactive Chat** - Chat with your video transcripts using natural language
- 🎯 **Newest to Oldest** - Videos are automatically sorted from newest to oldest
- 📊 **Metadata Storage** - Save video metadata for future reference

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

### Quick Start

Run the main application:
```bash
python main.py
```

The application will:
1. Prompt you for a YouTube channel URL
2. Ask how many videos to scrape
3. Scrape the channel and extract transcripts
4. Upload transcripts to Gemini AI
5. Start an interactive chat interface

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
│   ├── apify_scraper.py      # Apify YouTube scraping logic
│   ├── gemini_client.py      # Gemini API with file search
│   ├── video_processor.py    # Video transcript processing
│   └── chat_interface.py     # Interactive chat interface
├── data/
│   └── transcripts/          # Stored video transcripts
├── main.py                   # Main application entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## How It Works

1. **YouTube Scraping**
   - Uses Apify's `streamers/youtube-scraper` actor
   - Fetches video metadata and English subtitles
   - Sorts videos from newest to oldest

2. **Transcript Processing**
   - Creates individual text files for each video
   - Includes title, URL, description, and full transcript
   - Saves metadata in JSON format

3. **Gemini File Search**
   - Uploads transcript files to Gemini API
   - Uses Google's new file search feature
   - Enables semantic search across all videos

4. **Interactive Chat**
   - Natural language interface
   - Queries across all uploaded transcripts
   - Provides context-aware responses

## API References

- **Gemini File Search**: [Documentation](https://ai.google.dev/gemini-api/docs/file-search)
- **Apify API**: [Documentation](https://docs.apify.com)
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