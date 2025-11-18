"""
Chat Interface Module
Provides an interactive chat interface for querying video transcripts
"""

import sys
from typing import Optional
from .gemini_client import GeminiRAG


class ChatInterface:
    def __init__(self, gemini_client: GeminiRAG):
        """
        Initialize chat interface

        Args:
            gemini_client: Initialized GeminiRAG client with uploaded files
        """
        self.gemini_client = gemini_client
        self.conversation_history = []

    def start(self):
        """
        Start the interactive chat session
        """
        self._print_welcome()

        while True:
            try:
                # Get user input
                user_input = input("\n💬 You: ").strip()

                if not user_input:
                    continue

                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
                    print("\n👋 Thanks for chatting! Goodbye!")
                    break

                # Check for help command
                if user_input.lower() in ['help', '?']:
                    self._print_help()
                    continue

                # Check for list command
                if user_input.lower() == 'list':
                    self._list_files()
                    continue

                # Check for clear command
                if user_input.lower() == 'clear':
                    self.conversation_history = []
                    print("🗑️  Conversation history cleared!")
                    continue

                # Get response from Gemini
                print("\n🤔 Thinking...", end='', flush=True)
                response = self.gemini_client.chat(user_input)
                print("\r" + " " * 20 + "\r", end='')  # Clear "Thinking..." message

                # Store in conversation history
                self.conversation_history.append({
                    'user': user_input,
                    'assistant': response
                })

                # Print response
                print(f"🤖 Assistant: {response}")

            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again.")

    def _print_welcome(self):
        """Print welcome message"""
        print("\n" + "=" * 70)
        print("🎥 YouTube Channel RAG Chat")
        print("=" * 70)
        print("\nChat with your YouTube video transcripts using Gemini AI!")
        print(f"\n📊 {len(self.gemini_client.uploaded_files)} video transcript(s) loaded")
        print("\nCommands:")
        print("  • Type your question to chat with the videos")
        print("  • 'help' or '?' - Show help message")
        print("  • 'list' - List all uploaded files")
        print("  • 'clear' - Clear conversation history")
        print("  • 'exit' or 'quit' - Exit the chat")
        print("\n" + "=" * 70)

    def _print_help(self):
        """Print help message"""
        print("\n📖 Help - How to use this chat:")
        print("\n💡 Example questions you can ask:")
        print("  • What topics are covered in these videos?")
        print("  • Summarize the main points from [video title]")
        print("  • What did they say about [specific topic]?")
        print("  • Which video talks about [subject]?")
        print("  • Create a summary of all the videos")
        print("  • What are the key takeaways?")
        print("\n🎯 Tips:")
        print("  • Be specific in your questions for better results")
        print("  • You can ask follow-up questions")
        print("  • Reference specific video titles if needed")
        print("  • Ask for comparisons across multiple videos")

    def _list_files(self):
        """List all uploaded files"""
        print("\n📁 Uploaded Files:")
        if not self.gemini_client.uploaded_files:
            print("  No files uploaded yet.")
        else:
            for i, file in enumerate(self.gemini_client.uploaded_files, 1):
                print(f"  {i}. {file.display_name}")


def start_chat_session(gemini_client: GeminiRAG):
    """
    Start an interactive chat session

    Args:
        gemini_client: Initialized GeminiRAG client with uploaded files
    """
    chat = ChatInterface(gemini_client)
    chat.start()
