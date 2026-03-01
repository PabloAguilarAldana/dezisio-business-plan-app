import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Business Plan Excel Generator"
    DEBUG: bool = False
    
    # Excel Templates
    TEMPLATE_PATH: str = "templates/business_plan_template.xlsx"
    OUTPUT_DIR: str = "output"
    
    # Mapping
    FORM_SHEET_NAME: str = "FORM"
    REQUIRED_SHEETS: list[str] = ["FORM", "Projections", "PEM", "Sizes", "Listings"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Initialize settings
settings = Settings()

# Ensure output directory exists
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
