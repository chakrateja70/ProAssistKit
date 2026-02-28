def gmail_generator_prompt(context: str, resume_text: str, product: str) -> str:
    if product == "linkedin":
        return (
            f"Job Description:\n{context}\n\n"
            f"Resume:\n{resume_text}\n\n"
            "Generate a sweet and solid LinkedIn message expressing genuine interest in the role. "
            "DO NOT include a subject line - start directly with the greeting. "
            "Keep it warm, professional, and conversational - like reaching out to a connection. "
            "Carefully analyze the job description requirements and match them with specific skills, experiences, and achievements from the resume. "
            "Highlight 2 key elements from the resume that directly align with the job requirements, using concrete examples. "
            "Be concise but impactful - show enthusiasm and confidence without being overly formal. "
            "End with 'Resume attached. Thank you!' or similar warm closing. Keep the total message short and engaging."
        )
    elif product == "mail":
        return (
            f"Job Description:\n{context}\n\n"
            f"Resume:\n{resume_text}\n\n"
            "Generate a professional email applying for the job. Include a brief introduction expressing interest in the position. "
            "Carefully analyze the job description and identify key requirements. Then, highlight 2-3 key elements from the resume "
            "(skills, experiences, projects, or achievements) that directly align with and fulfill the job requirements. "
            "Use specific examples and concrete details from the resume to demonstrate qualification. "
            "\n\nIMPORTANT: If there are relevant PROJECTS in the resume, include a small overview of 1-2 key projects that demonstrate your capabilities "
            "and align with the job requirements. For each project mentioned, briefly describe what it does and the technologies/skills used, "
            "showing how it relates to the position you're applying for. Keep project descriptions concise but impactful."
            "\n\nInclude a polite closing expressing enthusiasm for the opportunity. "
            "Add a professional signature block with name, phone number, LinkedIn profile, and GitHub link (if available in resume). "
            "\n\nIMPORTANT: If you find an email address in the job description, extract it and return it on a new line at the very end in this exact format:\n"
            "RECEIVER_EMAIL: [email_address]\n"
            "If no email is found in the job description, return:\n"
            "RECEIVER_EMAIL: None"
        )
    else:
        raise ValueError(f"Unsupported product type: {product}")