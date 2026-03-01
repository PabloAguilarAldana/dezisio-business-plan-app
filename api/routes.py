import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from core.models import BusinessPlanInputs
from core.services import BusinessPlanService
from core.exceptions import ExcelGeneratorError

router = APIRouter()

@router.post("/generate", response_class=FileResponse)
async def generate_plan(
    inputs: BusinessPlanInputs, 
    service: BusinessPlanService = Depends()
):
    try:
        file_path = await service.generate_business_plan(inputs)
        
        # Verify file exists before returning
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="File was not created")
            
        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except ExcelGeneratorError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
