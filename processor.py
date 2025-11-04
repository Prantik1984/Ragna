from fastapi import FastAPI
from routes.health_check import router as health_router
from routes.file_uploader import router as file_uploader_router
from routes.document_querier import router as document_querier_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

allowed_origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    # allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    # allow_headers=["Content-Type", "Authorization"],
)

# Include the health check routes in the main application
app.include_router(health_router)

# Include the file uploader routes in the main application
app.include_router(file_uploader_router)

# Include the document query routes in the main application
app.include_router(document_querier_router)