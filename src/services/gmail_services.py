import base64
import os
from email.mime.text import MIMEText
from threading import Lock
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.config.settings import settings
from src.core import exceptions


class GmailService:

    SCOPES = settings.get_gmail_scopes()
    
    def __init__(self):
        self._service = None
        self._lock = Lock()  # thread-safe lazy init

    def _get_service(self):
        if self._service:
            return self._service

        with self._lock:
            if self._service:  # double-checked locking
                return self._service

            creds = self._load_credentials()
            self._service = build("gmail", "v1", credentials=creds, cache_discovery=False)
            return self._service

    def _load_credentials(self) -> Credentials:
        """Load credentials from env (production) or token.json (local dev)."""
        # Production: inject token JSON via environment variable
        token_json = os.getenv("GMAIL_TOKEN_JSON")
        if token_json:
            creds = Credentials.from_authorized_user_info(
                __import__("json").loads(token_json), settings.get_client_config(),
            )
        elif os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", settings.get_client_config())
        else:
            raise RuntimeError(
                "No Gmail credentials found. Set GMAIL_TOKEN_JSON env var or provide token.json."
            )

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        return creds

    def send_email(self, *, to: str, subject: str, body: str) -> str:
        """
        Send a plain-text email. Returns the sent message ID.
        Raises GmailSendError on failure.
        """
        try:
            message = MIMEText(body)
            message["to"] = to
            message["subject"] = subject

            raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
            result = (
                self._get_service()
                .users()
                .messages()
                .send(userId="me", body={"raw": raw})
                .execute()
            )
            print(f"Gmail API: Email sent successfully to {to} with subject '{subject}'")
            return result["id"]
        except HttpError as e:
            raise exceptions.GmailSendError(f"Gmail API error: {e.reason}") from e
        except Exception as e:
            raise exceptions.GmailSendError(f"Unexpected error sending email: {str(e)}") from e


gmail_service = GmailService()