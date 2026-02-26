from pathlib import Path
import re
import pypdf

from src.core.exceptions import PDFNotFoundError, PDFExtractionError
from src.schemas.response import PDFDocumentData


def load_pdf(file_path: str) -> PDFDocumentData:
    """Load PDF and extract all text"""
    path = Path(file_path)
    
    if not path.exists():
        raise PDFNotFoundError(f"File not found: {file_path}")
    
    try:
        with open(file_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            page_texts = []
            
            for page in reader.pages:
                text = page.extract_text()
                # Clean excessive spacing
                text = re.sub(r'(?<=\w)\s(?=\w)', '', text)
                text = re.sub(r' +', ' ', text)
                page_texts.append(text.strip())
            
            return PDFDocumentData(
                file_path=str(path),
                total_pages=len(reader.pages),
                text_content="\n\n".join(page_texts),
                page_texts=page_texts
            )
            
    except PDFNotFoundError:
        raise
    except Exception as e:
        raise PDFExtractionError(f"Failed to extract text: {str(e)}")


def get_pdf_text(file_path: str) -> str:
    """Extracts text from pdf"""
    doc = load_pdf(file_path)
    return doc.text_content
