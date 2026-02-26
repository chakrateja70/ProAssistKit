from fastapi import APIRouter, UploadFile, Form, HTTPException
import tempfile
import os

from src.services.llm_service import openai_service
from src.utils.document_processing import get_pdf_text
from src.schemas.response import (
    GmailGeneratorResponse, 
    GmailGeneratorData, 
    ProductType, 
    LinkedInRole, 
    MailRole
)
from src.core.exceptions import PDFNotFoundError, PDFExtractionError, LLMServiceAPIException, LLMServiceUnexpectedException

router = APIRouter()


@router.post("/gmail-generator", response_model=GmailGeneratorResponse, status_code=200)
async def gmail_generator(
    resume: UploadFile, 
    job_description: str = Form(..., description="Job description text"),
    product: ProductType = Form(..., description="Product type: linkedin or mail"),
    role: str = Form(..., description="Role: For linkedin (manager, ceo, TL, HR), For mail (HR only)")
):
    """
    Generate a professional LinkedIn message/Gmail based on resume, job description, product, and role.
    
    - **resume**: Upload resume file in PDF format
    - **job_description**: The job description text
    - **product**: Product type (linkedin or mail)
    - **role**: Target role - depends on product:
        - If product is "linkedin": manager, ceo, TL, or HR
        - If product is "mail": HR only
    """
    temp_file_path = None
    
    try:
        # Validate role based on product
        if product == ProductType.LINKEDIN:
            valid_roles = [r.value for r in LinkedInRole]
            if role not in valid_roles:
                raise HTTPException(
                    status_code=400, 
                    detail=f"For product 'linkedin', role must be one of: {', '.join(valid_roles)}"
                )
        elif product == ProductType.MAIL:
            valid_roles = [r.value for r in MailRole]
            if role not in valid_roles:
                raise HTTPException(
                    status_code=400, 
                    detail=f"For product 'mail', role must be: {', '.join(valid_roles)}"
                )
        
        # Validate file type
        if not resume.filename or not resume.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported for resume upload")
        
        # Create temporary file to store uploaded resume
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file_path = temp_file.name
            content = await resume.read()
            temp_file.write(content)
        
        # Extract text from resume PDF
        resume_text = get_pdf_text(temp_file_path)
        
        # Generate email using LLM service with dynamic role-based prompt
        generated_email = openai_service.generate_answer(
            job_description=job_description,
            resume_text=resume_text,
            product=product.value,
            role=role
        )
        
        return GmailGeneratorResponse(
            success_code=200,
            message="email successfully generated",
            data=GmailGeneratorData(
                generated_email=generated_email,
                resume_filename=resume.filename,
                product=product,
                role=role
            )
        )
        
    except PDFNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass  # Ignore cleanup errors

