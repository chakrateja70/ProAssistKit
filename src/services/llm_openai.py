from openai import OpenAI, APIError
from src.core.exceptions import LLMServiceAPIException, LLMServiceUnexpectedException
from src.config.settings import settings
from src.core.prompts import gmail_generator_prompt

class OpenAIService:
    """
    Service for OpenAI interactions using an optimized Singleton pattern.
    This ensures the OpenAI client is initialized only once.
    """
    _instance = None
    _client = None

    def __new__(cls):
        # This method ensures only one instance of OpenAIService is ever created
        if cls._instance is None:
            cls._instance = super(OpenAIService, cls).__new__(cls)
            cls._client = OpenAI(api_key=settings.OPENAI_API_KEY)
        return cls._instance

    def generate_answer(self, job_description: str, resume_text: str, product: str, role: str) -> str:
        """
        Generates an answer using the single, pre-initialized client.
        
        Args:
            job_description: The job description text
            resume_text: The extracted resume text
            product: Product type ("linkedin" or "mail")
            role: Target role ("manager", "ceo", "TL", or "HR")
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
                "linkedin": 300,      # Shorter message + "resume attached" line
                "mail": 500,          # Email body + full signature block (name, phone, LinkedIn, GitHub)
                "evaluation": 600     # Detailed evaluation content
            }
            max_tokens = token_limits.get(product, 500)
            
            chat_completion = self._client.chat.completions.create(
                messages=[{"role": "user", "content": formatted_prompt}],
                model=settings.OPENAI_MODEL,
                temperature=0.3,
                max_tokens=max_tokens,
                top_p=0.9,
            )
            print("Token usage:", chat_completion.usage)
            return chat_completion.choices[0].message.content.strip()

        except APIError as e:   
            raise LLMServiceAPIException(str(e))
        except Exception as e:
            raise LLMServiceUnexpectedException(str(e))

llm_service = OpenAIService()