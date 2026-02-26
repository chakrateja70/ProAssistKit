def gmail_generator_prompt(context: str, resume_text: str, product: str, role: str) -> str:
    """
    Generate dynamic prompt based on product type and target role.
    
    Supports: "linkedin", "mail", "evaluation"
    """
    
    # ============================================
    # RESUME EVALUATION MODE
    # ============================================
    if product == "evaluation":
        return f"""Analyze resume vs job description as {role.upper()}.

**RESUME:** {resume_text}
**JOB DESCRIPTION:** {context}

---

**CEO (150-200 words):** Strategic alignment, leadership potential, organizational value. Format: Overview + 3-4 strategic observations (bullets) + **Recommendation:** [Strongly Recommend/Recommend/Consider with Reservations/Do Not Recommend]. Tone: Strategic, business-focused.

**Manager (200-250 words):** Technical/soft skills vs team needs, manageability, onboarding, integration. Format: Summary + **Strengths** (3-4 bullets with evidence) + **Gaps/Concerns** + **Recommendation:** [Strong Yes/Yes/Maybe/No] with reasoning. Tone: Practical, team-focused.

**TL (250-300 words):** Technical skills/tools/tech vs JD, depth/breadth, problem-solving, stack fit. Format: Summary + **Technical Strengths** (bullets) + **Technical Gaps** + **Gap Severity:** [Critical/Moderate/Minor/None] + **Recommendation:** [Proceed to Tech Interview/Needs Screening Call/Proceed with Caution/Reject]. Tone: Technical, evidence-based.

**HR (200-250 words):** Experience/education/qualifications vs JD, communication (from resume quality), culture fit, red flags. Format: Summary + **Qualifications Match** (bullets) + **Culture Fit** (2-3 points) + **Concerns** (if any) + **Decision:** [Shortlist/Hold/Reject] with reasoning. Tone: Professional, balanced.

---

**Requirements:** ✅ Use specific data from resume/JD • Justify with evidence • Simple English • Note "Not mentioned" if missing. No generic statements • No assumptions • No bias • Stay in role.

**Output:**
[Evaluation content]

---
**CANDIDATE:** [Name]  
**POSITION:** [Job title]  
**EVALUATED BY:** {role.upper()}

Here is my resume attached below.
---"""
    
    # ============================================
    # EMAIL/LINKEDIN GENERATION MODE
    # ============================================
    role_guidance = {
        "manager": "professional and results-focused tone, highlighting leadership skills and achievements",
        "ceo": "executive-level tone, emphasizing strategic impact and high-level accomplishments",
        "TL": "technical yet approachable tone, showcasing expertise and collaborative abilities",
        "HR": "warm and professional tone, emphasizing cultural fit and genuine enthusiasm"
    }
    
    guidance = role_guidance.get(role, role_guidance["HR"])
    word_limit = "150" if product == "linkedin" else "250"
    message_type = "LinkedIn message" if product == "linkedin" else "email"
    
    if product == "linkedin":
        structure_instruction = """Return ONLY the message body with no subject line.

END WITH:
---
Here is my resume attached below."""
    else:
        structure_instruction = """Format:
Subject: [Clear, concise subject line mentioning the role]

[Email body]

MANDATORY SIGNATURE:
---
Here is my resume attached below.

[Full Name]
[Phone Number]
LinkedIn: [LinkedIn URL - if present]
GitHub: [GitHub URL - if present]

Extract ALL contact info from resume. If LinkedIn/GitHub exist, you MUST include them."""
    
    return f"""You are a professional career coach crafting a {message_type} to a {role.upper()} for a job application.

Use a {guidance}.

JOB DESCRIPTION:
{context}

RESUME:
{resume_text}

INSTRUCTIONS:
1. Clear, simple, easy-to-understand language
2. Express genuine interest in the role
3. Highlight experiences matching job requirements
4. Professional yet personable tone
5. Concise - under {word_limit} words for body
6. Avoid complex jargon
7. Show enthusiasm without being overly casual
8. Use only info from resume and JD

{structure_instruction}"""