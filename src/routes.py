from fastapi import APIRouter, UploadFile, Form, HTTPException
import tempfile
import os
import re
from src.services.llm_service import llm_service
from src.services.gmail_services import gmail_service
from src.core.exceptions import GmailSendError
from src.utils.document_processing import load_pdf
from src.schemas.response import (
    GmailGeneratorResponse,
    GmailGeneratorData,
    ProductType
)

router = APIRouter()


def extract_email(text: str) -> str | None:
    """Extract first valid email address from a block of text."""
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
    return match.group(0) if match else None


def strip_marker_line(text: str) -> str:
    """Remove RECEIVER_EMAIL marker line from LLM output if present."""
    return re.sub(r'\n*RECEIVER_EMAIL:[^\n]*', '', text).strip()


@router.post("/gmail-generator", response_model=GmailGeneratorResponse, status_code=200)
async def gmail_generator(
    resume: UploadFile,
    job_description: str = Form(..., description="Job description text"),
    product: ProductType = Form(..., description="Product type: linkedin or mail")):
        """Generate a professional LinkedIn message or Gmail based on resume, job description, and product."""
        temp_file_path = None

        try:
            if not resume.filename.endswith('.pdf'):  # type: ignore
                raise HTTPException(status_code=400, detail="Only PDF files are supported for resume upload")

            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file_path = temp_file.name
                temp_file.write(await resume.read())
            print(f"[FILE] ✓ Resume saved to: {temp_file_path}")

            resume_text = load_pdf(temp_file_path).text_content
            print(f"[PDF] ✓ Extracted {len(resume_text)} characters")

            generated_email = llm_service.generate_answer(
                job_description=job_description,
                resume_text=resume_text,
                product=product.value,
            )
            print(f"[LLM] ✓ Content generated ({len(generated_email)} characters)")

            # ── Mail: extract recipient and send 
            if product == ProductType.MAIL:
                # Strip LLM marker if present, then fall back to job description
                generated_email = strip_marker_line(generated_email)
                recipient = extract_email(job_description)

                if not recipient:
                    raise HTTPException(
                        status_code=422,
                        detail="No recipient email found in the job description. Please include one."
                    )

                try:
                    msg_id = gmail_service.send_email(
                        to=recipient,
                        subject="Application for the Position",
                        body=generated_email,
                    )
                    print(f"[GMAIL] ✓ Sent to {recipient} (msg_id={msg_id})")
                except GmailSendError as e:
                    raise HTTPException(status_code=502, detail=f"Email generation succeeded but sending failed: {str(e)}")

            return GmailGeneratorResponse(
                success_code=200,
                message="Email successfully generated and sent" if product == ProductType.MAIL else "Message successfully generated",
                data=GmailGeneratorData(
                    generated_email=generated_email,
                    resume_filename=resume.filename,  # type: ignore
                    product=product,
                ),
            )

        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except Exception:
                    pass