from fastapi import APIRouter, HTTPException, Request,File, UploadFile
from dotenv import load_dotenv
from Processors.PdfProcessor import PdfProcessor
from Processors.ChromaProcessor import ChromaProcessor
import os
router = APIRouter()

@router.post("/upload/pdfs")

async def uploadPdf(request: Request, file: UploadFile = File(...)):
    try:
        load_dotenv()
        max_upload_size = int(os.getenv("Max_Upload_size"))* 1024 * 1024
        await size_limit(request, max_upload_size)
        upload_dir=os.getenv("UploadDirectory")
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        pdf_processor = PdfProcessor()
        pdf_text= pdf_processor.read_pdf(file_path)
        pdf_chunks=pdf_processor.create_chunks(pdf_text,file_path)
        chroma_processor = ChromaProcessor()
        db_name=os.path.splitext(file.filename)[0]
        chroma_processor.SaveToDb(pdf_chunks, db_name)
        return {"uploaded": True,"id":db_name}
    except Exception as e:
        return {"uploaded":False,"error":str(e)}

async def size_limit(request: Request, max_bytes: int):
    cl = request.headers.get("content-length")
    if cl and int(cl) > max_bytes:
        raise HTTPException(status_code=413, detail="Upload too large.")
    return True