import PyPDF2
import uuid
from dotenv import load_dotenv
import os
class PdfProcessor:
    def read_pdf(self, pdf_file):
        reader = PyPDF2.PdfReader(pdf_file)
        text=""
        for page in reader.pages:
            text = text + page.extract_text() + "\n"
        return text

    def create_chunks(self, text,pdf_file):
        chunks = []
        start = 0
        load_dotenv()
        chunk_size = int(os.getenv("CHUNK_SIZE"))
        chunk_overlap = int(os.getenv("CHUNK_OVERLAP"))
        while start < len(text):
            end = start + chunk_size

            if start > 0:
                start = start - chunk_overlap

            chunk = text[start:end]

            if end < len(text):
                last_period = chunk.rfind(".")
                if last_period != -1:
                    chunk = chunk[: last_period + 1]
                    end = start + last_period + 1

            chunks.append(
                {
                    "text": chunk,
                    "id": uuid.uuid4(),
                    "meta_data": pdf_file,
                }
            )
            start = end
        return chunks
