import os
from fastapi import APIRouter, HTTPException, Depends
from core.models import BusinessPlanInputs
from core.services import BusinessPlanService
from core.exceptions import ExcelGeneratorError
from excel.preview import excel_to_html_preview

router = APIRouter()

@router.post("/generate")
async def generate_plan(
    inputs: BusinessPlanInputs, 
    service: BusinessPlanService = Depends()
):
    try:
        file_path = await service.generate_business_plan(inputs)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="File was not created")
            
        # Generate HTML Previews
        previews = excel_to_html_preview(file_path)
        
        # Return filename and previews
        # The frontend will use the filename to download from /download/filename
        return {
            "filename": os.path.basename(file_path),
            "downloadUrl": f"/download/{os.path.basename(file_path)}",
            "previews": previews
        }
    except ExcelGeneratorError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
