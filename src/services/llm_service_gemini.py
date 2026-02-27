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

    def generate_answer(self, job_description: str, resume_text: str, product: str) -> str:
        """
        Generates an answer using Gemini 2.5 Flash model.
        
        Args:
            job_description: The job description text
            resume_text: The extracted resume text
            product: Product type ("linkedin" or "mail")
        """
        try:
            formatted_prompt = gmail_generator_prompt(
                context=job_description,
                resume_text=resume_text,
                product=product
            )

            # Dynamic token limits based on product type (matching OpenAI service)
            token_limits = {
                "linkedin": 300,      # Shorter message + "resume attached" line
                "mail": 500,          # Email body + full signature block (name, phone, LinkedIn, GitHub)
            }
            max_tokens = token_limits.get(product, 500)
            
            generate_content_config = types.GenerateContentConfig(
                max_output_tokens=max_tokens,
                temperature=0.7,      # More creative/natural sounding text
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