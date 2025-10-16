import PyPDF2
class PdfProcessor:
    def read_pdf(self, pdf_file):
        reader = PyPDF2.PdfReader(pdf_file)
        text=""
        for page in reader.pages:
            text = text + page.extract_text()
        return text