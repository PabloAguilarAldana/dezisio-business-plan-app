import openpyxl
import logging
from app.config import settings
from excel.mapping import EXCEL_MAPPING
from core.exceptions import SheetNotFoundError, MappingError

logger = logging.getLogger(__name__)

def validate_excel_template(template_path: str):
    """
    Validates that the Excel template has all required sheets 
    and that mappings point to valid cells.
    """
    logger.info(f"Validating Excel template at {template_path}")
    
    try:
        wb = openpyxl.load_workbook(template_path, read_only=True)
    except FileNotFoundError:
        raise FileNotFoundError(f"Template not found at: {template_path}")
    except Exception as e:
        raise Exception(f"Error loading template: {str(e)}")

    # 1. Check Sheets
    existing_sheets = wb.sheetnames
    for required in settings.REQUIRED_SHEETS:
        if required not in existing_sheets:
            logger.error(f"Missing required sheet: {required}")
            raise SheetNotFoundError(f"Missing required sheet: {required}")

    # 2. Check Mapping Destinations
    # We assume all inputs are in the "FORM" sheet as per requirements
    form_sheet = wb[settings.FORM_SHEET_NAME]
    
    for key, (sheet_name, cell_coord) in EXCEL_MAPPING.items():
        if sheet_name not in existing_sheets:
            raise MappingError(f"Field '{key}' maps to non-existent sheet: {sheet_name}")
        
        # Verify cell exists/is accessible
        try:
            # In read_only mode, accessing a cell might not provide much validation 
            # other than it being a valid coordinate string.
            _ = form_sheet[cell_coord]
        except Exception:
            raise MappingError(f"Field '{key}' has invalid cell coordinate: {cell_coord}")

    logger.info("Template validation successful.")
    wb.close()
