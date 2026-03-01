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
            """Act as a recruitment expert. Write a job application email (<120 words) for the role in {context} using {resume_text}.
1. INTRO: One sentence connecting my background to the company's specific mission.
2. BODY: Two bullet points using the "Action-Context-Result" framework (e.g., "Reduced X by 25% using Y") to prove JD-Resume alignment.
3. PROJECT: One sentence on a high-impact project, stating the tech stack and its real-world outcome.
4. CONSTRAINTS: No generic fluff (passionate/hardworking); first-person; evidence-based only; signature included.
5. SIGNATURE: Name, phone, LinkedIn, GitHub (only if in resume).
6. EXTRACTION: At the very end, return "RECEIVER_EMAIL: [email]" if found in the JD, else "RECEIVER_EMAIL: None"."""
        )
    else:
        raise ValueError(f"Unsupported product type: {product}")