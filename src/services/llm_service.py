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

    def generate_answer(self, job_description: str, resume_text: str, product: str, role: str) -> str:
        """
        Generates an answer using Gemini 2.5 Flash model.
        """
        try:
            formatted_prompt = gmail_generator_prompt(
                context=job_description,
                resume_text=resume_text,
                product=product,
                role=role
            )


            # Dynamic token limits based on product type
            token_limits = {
                "linkedin": 3000,      # Increased for longer LinkedIn messages
                "mail": 4000,         # Increased for full email body and signature
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

            return response_text.strip() if response_text else "No response from Gemini model."

        except Exception as e:
            # Differentiate between API and unexpected errors if needed
            if "401" in str(e) or "403" in str(e):
                raise LLMServiceAPIException(f"Gemini API Error: {e}")
            raise LLMServiceUnexpectedException(f"Unexpected Gemini LLM Error: {e}")


# Create a single shared instance
llm_service = GeminiLLMService()