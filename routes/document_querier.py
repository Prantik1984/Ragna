from fastapi import APIRouter,Body
from Processors.ChromaProcessor import ChromaProcessor
router = APIRouter()

@router.post("/querydocument")

async def querydocument(
        document: str = Body(...),
        question: str = Body(...),
         ):
    chroma_processor = ChromaProcessor()
    results=chroma_processor.QueryDb(question,document)
    return  results
