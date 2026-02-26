from __future__ import annotations
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(override=True)

class Settings:
    """
    A centralized class to hold all application settings loaded from environment variables.
    """
    
    def __init__(self):
        # OpenAI settings (optional)
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
        self.OPENAI_MODEL: str = "gpt-4o-mini"

        # # Gemini LLM settings
        # self.GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "AIzaSyBY2ERUMGZKAJhzXyzAVzjcg6zctOjQqpM")
        # self.GEMINI_LLM_MODEL: str = os.getenv("GEMINI_LLM_MODEL", "gemini-2.5-flash")

    @staticmethod
    def _get_required(key: str) -> str:
        """Get a required environment variable or raise ValueError."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"{key} not found in environment variables. Please check your .env file.")
        return value


# Create a single instance of the settings to be imported across the application
settings = Settings()