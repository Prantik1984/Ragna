from fastapi import FastAPI
from routes.health_check import router as health_router
from routes.file_uploader import router as file_uploader_router
app = FastAPI()

# Include the health check routes in the main application
app.include_router(health_router)

# Include the file uploader routes in the main application
app.include_router(file_uploader_router)