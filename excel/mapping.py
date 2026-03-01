from typing import Dict, Tuple

# Mapping of model fields to Excel (Sheet, Cell)
# Values are stored as (SheetName, CellCoordinate)

EXCEL_MAPPING: Dict[str, Tuple[str, str]] = {
    "building_type": ("FORM", "C4"),
    "buildable_m2": ("FORM", "C5"),
    "building_status": ("FORM", "C6"),
    "purchase_price": ("FORM", "C7"),
    "exact_location": ("FORM", "C8"),
    "construction_project": ("FORM", "C9"),
    "bank_loan_needed": ("FORM", "C11"),
    "expected_loan_start_date": ("FORM", "C12"),
    "operation_mode": ("FORM", "C15"),
    "exit_year": ("FORM", "C19"),
}
