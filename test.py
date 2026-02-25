from src.utils.document_processing import load_pdf

pdf_data = load_pdf("sample.pdf")  # Replace with your PDF path
print(f"Pages: {pdf_data.total_pages}")
print(f"Text: {pdf_data.text_content}")