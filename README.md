# Business Plan Excel Generator

This application generates a production-ready Excel business plan based on a pre-existing template. It uses Clean Architecture principles and FastAPI for the API layer.

## Project Structure

```text
/business-plan-app
  /app
    main.py          # FastAPI initialization & Global Startup Validation
    config.py        # Settings and Env vars
  /api
    routes.py        # POST /generate endpoint
  /core
    models.py        # Pydantic V2 schemas (Input validation)
    services.py      # Business logic orchestration
    exceptions.py    # Custom domain exceptions
  /excel
    generator.py     # openpyxl engine to write cell values
    mapping.py       # CENTRALIZED MAPPING (Cell addresses)
    validators.py    # Template verification logic
  /templates
    business_plan_template.xlsx  # Your template goes here
  /output            # Generated files stored here
  requirements.txt
  README.md
```

## Setup & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare the Template
Place your Excel file in `templates/business_plan_template.xlsx`.
**MANDATORY**: Ensure the followings sheets exist: `FORM`, `Projections`, `PEM`, `Sizes`, `Listings`.

### 3. Run the App
```bash
cd business-plan-app
uvicorn app.main:app --reload
```

## API Usage Example

### POST `/generate`
Generates a new Excel file.

**Example CURL:**
```bash
curl -X 'POST' \
  'http://localhost:8000/generate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "buildingType": "4 star Hotel",
  "buildableM2": 2500.5,
  "buildingStatus": "Renovated",
  "purchasePrice": 1250000,
  "exactLocation": "Madrid, Spain",
  "constructionProject": true,
  "bankLoanNeeded": true,
  "expectedLoanStartDate": "2024-06-01",
  "operationMode": "Management",
  "exitYear": 2030
}' --output my_business_plan.xlsx
```

## Customization

### Changing Mappings
If you need to change which cells are written to, modify `excel/mapping.py`.
```python
EXCEL_MAPPING = {
    "building_type": ("FORM", "C4"),
    # ...
}
```

### Environment Variables
You can create a `.env` file to override defaults:
```env
TEMPLATE_PATH=templates/custom_template.xlsx
OUTPUT_DIR=./custom_output
```
