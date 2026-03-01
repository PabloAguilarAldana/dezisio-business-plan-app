import os
import uuid
from enum import Enum
import openpyxl
from datetime import datetime
from app.config import settings
from excel.mapping import EXCEL_MAPPING
from core.models import BusinessPlanInputs
from core.exceptions import ExcelGeneratorError

class ExcelGenerator:
    def __init__(self, template_path: str, output_dir: str):
        self.template_path = template_path
        self.output_dir = output_dir

    def generate(self, inputs: BusinessPlanInputs) -> str:
        """
        Loads the template, writes data, and returns the path to the output file.
        """
        try:
            wb = openpyxl.load_workbook(self.template_path)
        except Exception as e:
            raise ExcelGeneratorError(f"Failed to load template: {str(e)}")

        # Convert Pydantic model to dict for easier lookup
        # mode="python" keeps dates as date objects but handles enums better? 
        # Actually pydantic V2 model_dump() keeps objects.
        data = inputs.model_dump()
        
        # Apply Mapping
        for field_name, (sheet_name, cell_coord) in EXCEL_MAPPING.items():
            if sheet_name not in wb.sheetnames:
                continue
            
            sheet = wb[sheet_name]
            val = data.get(field_name)
            
            # Transformation logic
            if isinstance(val, bool):
                val = "Yes" if val else "No"
            elif isinstance(val, Enum):
                val = val.value
            
            # Writing value
            sheet[cell_coord].value = val

        # Generate unique filename
        filename = f"BusinessPlan_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.xlsx"
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            wb.save(output_path)
            wb.close()
        except Exception as e:
            raise ExcelGeneratorError(f"Failed to save generated file: {str(e)}")
            
        return output_path
