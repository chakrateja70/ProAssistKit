class PDFNotFoundError(Exception):
    """Raised when PDF file is not found"""
    pass


class PDFExtractionError(Exception):
    """Raised when text extraction fails"""
    pass
