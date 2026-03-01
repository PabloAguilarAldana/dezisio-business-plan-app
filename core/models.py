from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class BuildingType(str, Enum):
    TA = "TA"
    HOSTEL = "Hostel"
    HOTEL_3 = "3 star Hotel"
    HOTEL_4 = "4 star Hotel"
    LUXURY = "Luxury Hotel"

class BuildingStatus(str, Enum):
    PARTIALLY_RENOVATED = "Partially renovated"
    RENOVATED = "Renovated"
    PENDING = "Pending to be renovated"
    NOT_BUILT = "Not built"

class OperationMode(str, Enum):
    MANAGEMENT = "Management"
    LEASE = "Lease"

class BusinessPlanInputs(BaseModel):
    building_type: BuildingType = Field(..., alias="buildingType")
    buildable_m2: float = Field(..., gt=0, alias="buildableM2")
    building_status: BuildingStatus = Field(..., alias="buildingStatus")
    purchase_price: float = Field(..., ge=0, alias="purchasePrice")
    exact_location: str = Field("Based on client", alias="exactLocation")
    construction_project: bool = Field(..., alias="constructionProject")
    bank_loan_needed: bool = Field(..., alias="bankLoanNeeded")
    expected_loan_start_date: date = Field(..., alias="expectedLoanStartDate")
    operation_mode: OperationMode = Field(..., alias="operationMode")
    exit_year: int = Field(..., ge=2024, le=2100, alias="exitYear")

    @field_validator("construction_project", "bank_loan_needed", mode="after")
    @classmethod
    def format_bool_for_excel(cls, v: bool) -> str:
        # Note: In the generator we will convert bool to "Yes"/"No"
        # but here we keep type as bool for API validation.
        return v

    class Config:
        populate_by_name = True
