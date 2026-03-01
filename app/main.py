import logging
from fastapi import FastAPI
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

# Include routes
app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
