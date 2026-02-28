from pydantic import BaseModel, Field
from typing import Optional, Any, List
from enum import Enum

class ProductType(str, Enum):
    """Product types for message generation"""
    LINKEDIN = "linkedin"
    MAIL = "mail"

class ResponseBase(BaseModel):
    """Base response model"""
    success: bool
    message: str
    data: Optional[Any] = None

class PDFDocumentData(BaseModel):
    """PDF document data structure"""
    file_path: str
    total_pages: int
    text_content: str
    page_texts: List[str] = Field(default_factory=list)

class GmailGeneratorData(BaseModel):
    """Gmail generator response data"""
    generated_email: str
    resume_filename: str
    product: ProductType
    
class GmailGeneratorResponse(BaseModel):
    """Gmail generator endpoint response"""
    success_code: int = Field(default=200, description="Success status code")
    message: str = Field(default="email successfully generated")
    data: GmailGeneratorData

class GmailSenderError(BaseModel):
    """Gmail sender error response"""
    success_code: int = Field(default=500, description="Error status code")
    message: str = Field(default="Failed to send email")
    error_details: Optional[str] = None