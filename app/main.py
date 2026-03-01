import logging
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from api.routes import router
from excel.validators import validate_excel_template

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME)

@app.on_event("startup")
async def startup_event():
    """
    On startup, validate the existence and structure of the Excel template.
    If validation fails, the app will not start.
    """
    try:
        validate_excel_template(settings.TEMPLATE_PATH)
    except Exception as e:
        logger.error(f"CRITICAL: Template validation failed: {str(e)}")
        # In production, we might want to exit or raise
        import sys
        sys.exit(1)

# Include API routes
app.include_router(router)

# Serve Static Files
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not found. Please check static/ directory."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
