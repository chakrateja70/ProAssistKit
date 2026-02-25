from src.services.llm_service import OpenAIService

def test_openai_service_initialization():
    content = "Chakra Teja is a AI Engineer"
    question = "What is the profession of Chakra Teja?"
    openai_service = OpenAIService()
    test = openai_service.generate_answer(content, question)

    print(test)

test_openai_service_initialization()