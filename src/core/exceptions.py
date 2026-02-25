# HTTP status codes
HTTP_404_NOT_FOUND = 404
HTTP_500_INTERNAL_SERVER_ERROR = 500

# Status messages
STATUS_MESSAGES = {
    HTTP_404_NOT_FOUND: "Not Found",
    HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error"
}

class BaseAPIException(Exception):
    """Base exception for all API errors"""
    def __init__(self, status_code: int, status_message: str, error_message: str):
        self.status_code = status_code
        self.status_message = status_message
        self.error_message = error_message
        super().__init__(self.error_message)


class PDFNotFoundError(BaseAPIException):
    """Exception when PDF file is not found"""
    def __init__(self, error_message: str = "PDF file not found"):
        super().__init__(
            status_code=HTTP_404_NOT_FOUND,
            status_message=STATUS_MESSAGES[HTTP_404_NOT_FOUND],
            error_message=error_message
        )
class PDFExtractionError(BaseAPIException):
    """Exception when text extraction fails"""
    def __init__(self, error_message: str = "Failed to extract text from PDF"):
        super().__init__(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            status_message=STATUS_MESSAGES[HTTP_500_INTERNAL_SERVER_ERROR],
            error_message=error_message
        )
