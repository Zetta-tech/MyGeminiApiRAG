"""
Video Processor Module
Processes YouTube videos and creates transcript files for Gemini file search
"""

import os
import json
from typing import List, Dict
from datetime import datetime


class VideoProcessor:
    def __init__(self, output_dir: str = "data/transcripts"):
        """
        Initialize video processor

        Args:
            output_dir: Directory to save transcript files
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def create_transcript_file(self, video: Dict) -> str:
        """
        Create a transcript file for a video

        Args:
            video: Video dictionary with title, url, description, and subtitles

        Returns:
            Path to the created transcript file
        """
        # Create a safe filename from video title
        safe_title = self._sanitize_filename(video.get('title', 'Untitled'))
        video_id = video.get('id', 'unknown')
        filename = f"{safe_title}_{video_id}.txt"
        filepath = os.path.join(self.output_dir, filename)

        # Create transcript content
        content = self._format_transcript(video)

        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"💾 Created transcript: {filename}")
        return filepath

    def create_all_transcript_files(self, videos: List[Dict]) -> List[str]:
        """
        Create transcript files for all videos

        Args:
            videos: List of video dictionaries

        Returns:
            List of file paths created
        """
        print(f"\n📝 Creating transcript files for {len(videos)} videos...")
        file_paths = []

        for i, video in enumerate(videos, 1):
            print(f"\n[{i}/{len(videos)}] Processing: {video.get('title', 'Untitled')}")

            # Skip videos without subtitles
            if not video.get('subtitles'):
                print("⚠️  No subtitles available, skipping...")
                continue

            try:
                filepath = self.create_transcript_file(video)
                file_paths.append(filepath)
            except Exception as e:
                print(f"❌ Error creating transcript: {e}")
                continue

        print(f"\n✅ Created {len(file_paths)} transcript files!")
        return file_paths

    def _sanitize_filename(self, filename: str, max_length: int = 50) -> str:
        """
        Sanitize filename by removing invalid characters

        Args:
            filename: Original filename
            max_length: Maximum length of filename

        Returns:
            Sanitized filename
        """
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')

        # Replace spaces with underscores
        filename = filename.replace(' ', '_')

        # Limit length
        if len(filename) > max_length:
            filename = filename[:max_length]

        return filename

    def _format_transcript(self, video: Dict) -> str:
        """
        Format video data into a transcript file

        Args:
            video: Video dictionary

        Returns:
            Formatted transcript content
        """
        title = video.get('title', 'Untitled')
        url = video.get('url', '')
        description = video.get('description', '')
        date = video.get('date', '')
        views = video.get('views', 0)
        duration = video.get('duration', '')
        subtitles = video.get('subtitles', '')

        content = f"""# {title}

**URL:** {url}
**Date:** {date}
**Views:** {views:,}
**Duration:** {duration}

## Description

{description}

## Transcript

{subtitles}

---
Video ID: {video.get('id', '')}
"""
        return content

    def save_metadata(self, videos: List[Dict], filename: str = "metadata.json"):
        """
        Save video metadata to JSON file

        Args:
            videos: List of video dictionaries
            filename: Name of the metadata file
        """
        filepath = os.path.join(self.output_dir, filename)

        metadata = {
            'total_videos': len(videos),
            'processed_date': datetime.now().isoformat(),
            'videos': videos
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"💾 Saved metadata to: {filename}")

    def get_all_transcript_files(self) -> List[str]:
        """
        Get all transcript files in the output directory

        Returns:
            List of transcript file paths
        """
        if not os.path.exists(self.output_dir):
            return []

        files = []
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.txt'):
                files.append(os.path.join(self.output_dir, filename))

        return sorted(files)
