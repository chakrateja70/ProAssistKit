def gmail_generator_prompt(context: str, resume_text: str, product: str) -> str:
    """
    Generate dynamic prompt based on product type.
    Supports: "linkedin", "mail"
    """
    guidance = "professional and engaging, emphasizing relevant experience and genuine interest"
    word_limit = 150 if product == "linkedin" else 250
    
    if product == "linkedin":
        structure_instruction = "Return ONLY the message body with no subject line."
    else:
        structure_instruction = """Format:
            Subject: [Concise subject mentioning the role]

            [Email body]

            ---
            Please find my resume attached below.

            [Full Name]
            [Phone Number]
            LinkedIn: [URL if available in resume]
            GitHub: [URL if available in resume]

            Include all contact details found in resume."""
                
    return f"""Craft a professional {product} message for this job application.

            Tone: {guidance}

            JOB DESCRIPTION:
            {context}

            RESUME:
            {resume_text}

            REQUIREMENTS:
            - Use clear, simple language - avoid jargon
            - Express genuine interest in the role with specific reasons
            - Match 2-3 relevant resume experiences to job requirements with concrete examples
            - Professional yet personable tone
            - MAXIMUM {word_limit} words for body content
            - Use ONLY information from resume and job description - do not fabricate details
            - Show enthusiasm without being overly casual

            {structure_instruction}"""