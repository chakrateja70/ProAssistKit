from __future__ import annotations
import os
import json
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

        # Gemini LLM settings
        self.GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY","")
        self.GEMINI_LLM_MODEL: str = "gemini-2.5-flash"

        self._DEFAULT_GMAIL_SCOPES = [
            "https://www.googleapis.com/auth/gmail.send"]

        # Gmail API settings
        self.GMAIL_CLIENT_ID: str = os.getenv("GMAIL_CLIENT_ID", "")
        self.GMAIL_CLIENT_SECRET: str = os.getenv("GMAIL_CLIENT_SECRET", "")
        self.GMAIL_PROJECT_ID: str = os.getenv("GMAIL_PROJECT_ID", "")
        self.GMAIL_AUTH_URI: str = os.getenv("GMAIL_AUTH_URI", "")
        self.GMAIL_TOKEN_URI: str = os.getenv("GMAIL_TOKEN_URI", "")
        self.GMAIL_AUTH_PROVIDER_X509_CERT_URL: str = os.getenv("GMAIL_AUTH_PROVIDER_X509_CERT_URL", "")
        self.GMAIL_REDIRECT_URIS = json.loads(os.getenv("GMAIL_REDIRECT_URIS", "[]"))
        self.GMAIL_JAVASCRIPT_ORIGINS = json.loads(os.getenv("GMAIL_JAVASCRIPT_ORIGINS", "[]"))


    def get_client_config(self) -> dict:
        return {    
            "web": {
                "client_id": self.GMAIL_CLIENT_ID,
                "project_id": self.GMAIL_PROJECT_ID,
                "auth_uri": self.GMAIL_AUTH_URI,
                "token_uri": self.GMAIL_TOKEN_URI,
                "auth_provider_x509_cert_url": self.GMAIL_AUTH_PROVIDER_X509_CERT_URL,
                "client_secret": self.GMAIL_CLIENT_SECRET,
                "redirect_uris": self.GMAIL_REDIRECT_URIS if isinstance(self.GMAIL_REDIRECT_URIS, list) else [],
                "javascript_origins": self.GMAIL_JAVASCRIPT_ORIGINS,
            }
        }
    
    def get_gmail_scopes(self) -> list[str]:
        raw = os.getenv("GMAIL_SCOPES", "").strip()
        if not raw:
            return self._DEFAULT_GMAIL_SCOPES
        # Accept JSON array or comma-separated list
        try:
            if raw.startswith("["):
                arr = json.loads(raw)
                return [s.strip() for s in arr if isinstance(s, str) and s.strip()]
            return [s.strip() for s in raw.split(",") if s.strip()]
        except Exception:
            return self._DEFAULT_GMAIL_SCOPES



    @staticmethod
    def _get_required(key: str) -> str:
        """Get a required environment variable or raise ValueError."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"{key} not found in environment variables. Please check your .env file.")
        return value
    



# Create a single instance of the settings to be imported across the application
settings = Settings()