from fastapi import APIRouter, HTTPException, Request,File, UploadFile
from dotenv import load_dotenv
import os
router = APIRouter()

@router.post("/upload/pdfs")

async def uploadPdf(request: Request, file: UploadFile = File(...)):
    load_dotenv()
    max_upload_size = int(os.getenv("Max_Upload_size"))* 1024 * 1024
    await size_limit(request, max_upload_size)
    upload_dir=os.getenv("UploadDirectory")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"status": "File Uploaded Successfully"}

async def size_limit(request: Request, max_bytes: int):
    cl = request.headers.get("content-length")
    if cl and int(cl) > max_bytes:
        raise HTTPException(status_code=413, detail="Upload too large.")
    return True