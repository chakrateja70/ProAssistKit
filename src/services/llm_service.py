from google import genai
from google.genai import types
from src.config.settings import settings
from src.core.exceptions import LLMServiceAPIException, LLMServiceUnexpectedException
from src.core.prompts import gmail_generator_prompt

class GeminiLLMService:
    """
    Service for interacting with the Gemini LLM (gemini-2.5-flash).
    Implements a Singleton pattern to ensure only one client is initialized.
    """

    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiLLMService, cls).__new__(cls)
            cls._client = genai.Client(api_key=settings.GEMINI_API_KEY)
        return cls._instance


    def generate_answer(self, job_description: str, resume_text: str, product: str):
        """
        Generates an answer using Gemini 2.5 Flash model.
        Returns a dict with 'response_text' and 'receiver_mail'.
        """
        try:
            formatted_prompt = gmail_generator_prompt(
                context=job_description,
                resume_text=resume_text,
                product=product
            )

            # Dynamic token limits based on product type
            token_limits = {
                "linkedin": 3000,
                "mail": 4000,
            }
            max_tokens = token_limits.get(product, 1000)
            generate_content_config = types.GenerateContentConfig(
                max_output_tokens=max_tokens
            )

            # Stream the response and collect chunks
            response_text = ""
            for chunk in self._client.models.generate_content_stream(
                model=settings.GEMINI_LLM_MODEL,
                contents=formatted_prompt,
                config=generate_content_config,
            ):
                if hasattr(chunk, "text") and chunk.text:
                    response_text += chunk.text

            response_text = response_text.strip() if response_text else "No response from Gemini model."

            # Extract receiver email from job description
            import re
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails_found = re.findall(email_pattern, job_description)
            receiver_mail = emails_found[0] if emails_found else None

            return {
                "response_text": response_text,
                "receiver_mail": receiver_mail
            }

        except Exception as e:
            if "401" in str(e) or "403" in str(e):
                raise LLMServiceAPIException(f"Gemini API Error: {e}")
            raise LLMServiceUnexpectedException(f"Unexpected Gemini LLM Error: {e}")


# Create a single shared instance
llm_service = GeminiLLMService()