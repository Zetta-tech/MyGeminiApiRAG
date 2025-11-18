"""
Gemini API Client Module
Handles file upload and chat with file search using Google's Gemini API
"""

import os
import google.generativeai as genai
from typing import List, Optional, Dict
import time


class GeminiRAG:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client with API key

        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.uploaded_files = []

    def upload_file(self, file_path: str, display_name: Optional[str] = None) -> Dict:
        """
        Upload a file to Gemini API for file search

        Args:
            file_path: Path to the file to upload
            display_name: Optional display name for the file

        Returns:
            Uploaded file object
        """
        print(f"📤 Uploading file: {file_path}")

        try:
            # Upload file
            uploaded_file = genai.upload_file(
                path=file_path,
                display_name=display_name or os.path.basename(file_path)
            )

            # Wait for file to be processed
            while uploaded_file.state.name == "PROCESSING":
                print("⏳ Processing file...")
                time.sleep(2)
                uploaded_file = genai.get_file(uploaded_file.name)

            if uploaded_file.state.name == "FAILED":
                raise ValueError(f"File processing failed: {uploaded_file.state.name}")

            print(f"✅ File uploaded successfully: {uploaded_file.display_name}")
            self.uploaded_files.append(uploaded_file)
            return uploaded_file

        except Exception as e:
            print(f"❌ Error uploading file: {e}")
            raise

    def upload_multiple_files(self, file_paths: List[str]) -> List[Dict]:
        """
        Upload multiple files to Gemini API

        Args:
            file_paths: List of file paths to upload

        Returns:
            List of uploaded file objects
        """
        uploaded = []
        for i, file_path in enumerate(file_paths, 1):
            print(f"\n[{i}/{len(file_paths)}]")
            try:
                uploaded_file = self.upload_file(file_path)
                uploaded.append(uploaded_file)
            except Exception as e:
                print(f"⚠️  Skipping file due to error: {e}")
                continue

        return uploaded

    def chat(self, message: str, files: Optional[List] = None) -> str:
        """
        Chat with the model using uploaded files as context

        Args:
            message: User message/question
            files: Optional list of specific files to use (defaults to all uploaded files)

        Returns:
            Model response
        """
        context_files = files or self.uploaded_files

        if not context_files:
            print("⚠️  No files available for context. Answering without file search.")
            response = self.model.generate_content(message)
            return response.text

        # Create prompt with file references
        print(f"💬 Querying {len(context_files)} files...")

        try:
            # Use the files as context for the chat
            response = self.model.generate_content([message] + context_files)
            return response.text
        except Exception as e:
            print(f"❌ Error during chat: {e}")
            raise

    def list_uploaded_files(self) -> List[Dict]:
        """
        List all files uploaded to Gemini API

        Returns:
            List of uploaded file metadata
        """
        files = []
        for file in genai.list_files():
            files.append({
                'name': file.name,
                'display_name': file.display_name,
                'uri': file.uri,
                'state': file.state.name,
            })
        return files

    def delete_file(self, file_name: str):
        """
        Delete a file from Gemini API

        Args:
            file_name: Name of the file to delete
        """
        try:
            genai.delete_file(file_name)
            print(f"🗑️  Deleted file: {file_name}")
        except Exception as e:
            print(f"❌ Error deleting file: {e}")

    def clear_all_files(self):
        """
        Delete all uploaded files from Gemini API
        """
        print("🗑️  Clearing all uploaded files...")
        for file in genai.list_files():
            try:
                self.delete_file(file.name)
            except Exception as e:
                print(f"⚠️  Error deleting {file.name}: {e}")

        self.uploaded_files = []
        print("✅ All files cleared!")
