from fastapi import APIRouter, UploadFile, Form, HTTPException
import tempfile
import os
from src.services.llm_service import llm_service
from src.utils.document_processing import load_pdf
from src.schemas.response import (
    GmailGeneratorResponse, 
    GmailGeneratorData, 
    ProductType, 
    LinkedInRole, 
    MailRole
)

router = APIRouter()

def validate_role_for_product(product: ProductType, role: str) -> None:
    """Validate role is appropriate for the given product type."""
    valid_roles = [r.value for r in (LinkedInRole if product == ProductType.LINKEDIN else MailRole)]
    if role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role for {product.value}: {', '.join(valid_roles)}")

@router.post("/gmail-generator", response_model=GmailGeneratorResponse, status_code=200)
async def gmail_generator(
    resume: UploadFile, 
    job_description: str = Form(..., description="Job description text"),
    product: ProductType = Form(..., description="Product type: linkedin or mail"),
    role: str = Form(..., description="Role: For linkedin (manager, ceo, TL, HR), For mail (HR only)")):
        
        """Generate a professional LinkedIn message or Gmail based on resume, job description, product, and role."""
        temp_file_path = None
        
        try:
            # Validate role based on product
            validate_role_for_product(product, role)
            
            # Validate file type
            if not resume.filename.endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are supported for resume upload")
            
            # Create temporary file to store uploaded resume
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file_path = temp_file.name
                content = await resume.read()
                temp_file.write(content)
            print(f"[FILE] ✓ Resume saved to temporary location: {temp_file_path}")
            
            # Extract text from resume PDF
            resume_text = load_pdf(temp_file_path).text_content
            print(f"[PDF] Text extracted successfully ({len(resume_text)} characters)")
            
            # Generate email using LLM service with dynamic role-based prompt
            generated_email = llm_service.generate_answer(
                job_description=job_description,
                resume_text=resume_text,
                product=product.value,
                role=role
            )
            print(f"[LLM] ✓ Email generated successfully ({len(generated_email)} characters)")
            
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
        
        finally:
            # Clean up temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except Exception:
                    pass  # Ignore cleanup errors

