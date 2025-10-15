from fastapi import APIRouter, HTTPException, Request
from dotenv import load_dotenv
import os
router = APIRouter()

@router.post("/upload/pdfs")

def uploadPdf():
    load_dotenv()
    max_upload_size = os.getenv("Max_Upload_size")* 1024 * 1024
    return {"status": db_url}

async def size_limit(request: Request, max_bytes: int = 20 * 1024 * 1024):
    cl = request.headers.get("content-length")
    if cl and int(cl) > max_bytes:
        raise HTTPException(status_code=413, detail="Upload too large.")
    return True