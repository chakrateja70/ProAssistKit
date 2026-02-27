from fastapi import HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_403_FORBIDDEN
)

# Centralized status messages
STATUS_MESSAGES = {
    HTTP_400_BAD_REQUEST: "Bad Request",
    HTTP_404_NOT_FOUND: "Not Found",
    HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
    HTTP_403_FORBIDDEN: "Forbidden"
}

# Base Exception Class
class BaseAPIException(HTTPException):
    """Base exception class for all API exceptions."""
    def __init__(self, status_code: int, status_message: str, error_message: str):
        super().__init__(
            status_code=status_code,
            detail={
                "statusCode": status_code,
                "statusMessage": status_message,
                "errorMessage": error_message
            }
        )

# Exception for LLM Service API error
class LLMServiceAPIException(BaseAPIException):
    """Exception for errors communicating with the AI service."""
    def __init__(self, error_message: str):
        super().__init__(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            status_message=STATUS_MESSAGES[HTTP_500_INTERNAL_SERVER_ERROR],
            error_message=error_message 
        )

# Exception for LLM Service unexpected error
class LLMServiceUnexpectedException(BaseAPIException):
    """Exception for unexpected errors during answer generation."""
    def __init__(self, error_message: str):
        super().__init__(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            status_message=STATUS_MESSAGES[HTTP_500_INTERNAL_SERVER_ERROR],
            error_message=error_message
        )

class PDFExtractionError(BaseAPIException):
    """Exception when text extraction fails"""
    def __init__(self, error_message: str = "Failed to extract text from PDF"):
        super().__init__(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            status_message=STATUS_MESSAGES[HTTP_500_INTERNAL_SERVER_ERROR],
            error_message= error_message
        )

class PDFNotFoundError(BaseAPIException):
    """Exception when PDF file is not found"""
    def __init__(self, error_message: str = "PDF file not found"):
        super().__init__(
            status_code=HTTP_404_NOT_FOUND,
            status_message=STATUS_MESSAGES[HTTP_404_NOT_FOUND],
            error_message=error_message
        )