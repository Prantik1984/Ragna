import PyPDF2
import uuid
from dotenv import load_dotenv
import os
import io
class PdfProcessor:
    def read_pdf(self, file_bytes):
        pdf_stream = io.BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_stream)
        text=""
        for page in reader.pages:
            text = text + page.extract_text() + "\n"
        return text

    def create_chunks(self, text,pdf_file):
        chunks = []
        start = 0
        n = len(text)
        load_dotenv()

        chunk_size = int(os.getenv("CHUNK_SIZE"))
        chunk_overlap = int(os.getenv("CHUNK_OVERLAP"))

        if not text:
            return []

        chunk_size = max(1, chunk_size)
        chunk_overlap = max(0, min(chunk_overlap, chunk_size - 1))
        while start < n:
            end = min(start + chunk_size, n)
            chunk = text[start:end]
            if end < n:
                last_period = chunk.rfind(".")
                last_space = chunk.rfind(" ")
                boundary = max(last_period, last_space)
                if boundary != -1 and boundary > chunk_size * 0.6:
                    end = start + boundary + 1
                    chunk = text[start:end]
            chunks.append({
                "id": str(uuid.uuid4()),
                "text": chunk.strip(),
                "meta_data": pdf_file,
            })
            start = max(end - chunk_overlap, start + 1)

        return chunks
