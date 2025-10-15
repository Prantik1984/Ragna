from fastapi import FastAPI
from routes.health_check import router as health_router
from routes.file_uploader import router as file_uploader_router
app = FastAPI()

app.include_router(health_router)
app.include_router(file_uploader_router)