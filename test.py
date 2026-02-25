from src.utils.document_processing import load_pdf

pdf_data = load_pdf(r"c:\Users\kundr\Downloads\TEJA_AI.pdf")
print(pdf_data.text_content)