def gmail_generator_prompt(context: str, resume_text: str, product: str, role: str) -> str:
    """
    Generate dynamic prompt based on product type and target role.
    Supports: "linkedin", "mail"
    """
    role_guidance = {
        "manager": "professional, results-focused, highlighting leadership and achievements",
        "ceo": "executive-level, emphasizing strategic impact and accomplishments",
        "TL": "technical yet approachable, showcasing expertise and collaboration",
        "HR": "warm and professional, emphasizing cultural fit and enthusiasm"
    }
    
    guidance = role_guidance.get(role, role_guidance["HR"])
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
                
    return f"""Craft a professional {product} message to a {role.upper()} for this job application.

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