def gmail_generator_prompt(context: str, resume_text: str, product: str, role: str) -> str:
    """Generate dynamic prompt based on product type and target role."""
    
    # Role-specific guidance
    role_guidance = {
        "manager": "results-oriented tone focusing on leadership, team management, and strategic accomplishments",
        "ceo": "executive-level tone emphasizing high-level achievements, business impact, and strategic vision",
        "TL": "technical and collaborative tone highlighting expertise, mentorship, and project leadership",
        "HR": "professional and personable tone focusing on cultural fit, soft skills, and genuine interest"
    }
    
    guidance = role_guidance.get(role, role_guidance["HR"])
    word_limit = "150" if product == "linkedin" else "200"
    message_type = "LinkedIn message" if product == "linkedin" else "email"
    
    return f"""You are a career coach crafting a {message_type} to a {role.upper()} for a job application.

Use a {guidance}.

JOB DESCRIPTION:
{context}

RESUME:
{resume_text}

REQUIREMENTS:
- Under {word_limit} words
- Match skills/experiences from resume to job description
- Tailor for {role.upper()} level communication
- No placeholders, greetings, signatures, or subject lines
- Use only information from provided resume and job description

Return the message body only."""