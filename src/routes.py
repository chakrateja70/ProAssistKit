from fastapi import APIRouter, UploadFile, Form, HTTPException
import tempfile
import os
import re
from src.services.llm_service import llm_service
from src.utils.document_processing import load_pdf
from src.schemas.response import (
    GmailGeneratorResponse, 
    GmailGeneratorData, 
    ProductType
)

router = APIRouter()

@router.post("/gmail-generator", response_model=GmailGeneratorResponse, status_code=200)
async def gmail_generator(
    resume: UploadFile, 
    job_description: str = Form(..., description="Job description text"),
    product: ProductType = Form(..., description="Product type: linkedin or mail")):
        
        """Generate a professional LinkedIn message or Gmail based on resume, job description, and product."""
        temp_file_path = None
        
        try:
            
            # Validate file type
            if not resume.filename.endswith('.pdf'): #type: ignore
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
            
            # Generate email using LLM service
            result = llm_service.generate_answer(
                job_description=job_description,
                resume_text=resume_text,
                product=product.value
            )
            generated_email = result["response_text"]
            receiver_gmail = result["receiver_mail"] if product == ProductType.MAIL else None
            print(f"[LLM] ✓ Email generated successfully ({len(generated_email)} characters)")
            print(f"[EMAIL] Receiver email: {receiver_gmail}")

            return GmailGeneratorResponse(
                success_code=200,
                message="email successfully generated",
                data=GmailGeneratorData(
                    generated_email=generated_email,
                    resume_filename=resume.filename, #type: ignore
                    product=product,
                    receiver_email=receiver_gmail
                )
            )
        
        finally:
            # Clean up temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except Exception:
                    pass  # Ignore cleanup errors

