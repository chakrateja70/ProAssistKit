from pydantic import BaseModel, Field
from typing import Optional, Any, List


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
