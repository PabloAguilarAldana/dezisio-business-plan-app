from app.config import settings
from excel.generator import ExcelGenerator
from core.models import BusinessPlanInputs

class BusinessPlanService:
    def __init__(self):
        self.generator = ExcelGenerator(
            template_path=settings.TEMPLATE_PATH,
            output_dir=settings.OUTPUT_DIR
        )

    async def generate_business_plan(self, inputs: BusinessPlanInputs) -> str:
        """
        Main entry point for generating the Excel file.
        Orchestrates validation (via Pydantic) and Excel generation.
        """
        # Logic to generate Excel
        # In a real sync scenario openpyxl might block, 
        # but for this scale it's generally fine.
        output_path = self.generator.generate(inputs)
        return output_path
