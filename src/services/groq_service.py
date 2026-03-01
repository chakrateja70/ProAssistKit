import os
import requests
from src.config.settings import settings
from src.core.exceptions import LLMServiceAPIException, LLMServiceUnexpectedException
from src.core.prompts import gmail_generator_prompt


class GroqLLMService:
    """
    Service for interacting with the Groq LLM API.
    Implements a Singleton pattern to ensure only one client is initialized.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GroqLLMService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_api_key"):
            api_key = os.getenv("GROQ_API_KEY") or getattr(settings, "GROQ_API_KEY", None)
            if not api_key:
                raise LLMServiceAPIException("Groq API key not found in environment or settings.")
            self._api_key = api_key
            self._base_url = "https://api.groq.com/openai/v1/chat/completions"

    def generate_answer(self, job_description: str, resume_text: str, product: str) -> str:
        """
        Generates an answer using the Groq LLM API.
        """
        try:
            formatted_prompt = gmail_generator_prompt(
                context=job_description,
                resume_text=resume_text,
                product=product
            )
            model = getattr(settings, "GROQ_LLM_MODEL", "llama-3.3-70b-versatile")
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are Groq, a highly intelligent, helpful AI assistant."},
                    {"role": "user", "content": formatted_prompt}
                ],
                "temperature": 0.7
            }
            response = requests.post(self._base_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            raise LLMServiceUnexpectedException(f"Unexpected Groq LLM Error: {e}")

llm_service = GroqLLMService()  