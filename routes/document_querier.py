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

@router.get("/listdocuments")

async def listdocuments():
    """"
    List all documents in the db
    """
    chroma_processor = ChromaProcessor()
    results=chroma_processor.get_all_documents()
    return results
