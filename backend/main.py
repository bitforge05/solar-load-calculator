from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
import uuid
from services.extractor import BillExtractor
from services.excel_handler import ExcelHandler

app = FastAPI(root_path="/api" if os.environ.get("VERCEL") else "")

# Enable CORS for frontend integration
origins = [
    "https://solar-load-calculator.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use /tmp for Vercel/Serverless compatibility
if os.environ.get("VERCEL"):
    UPLOAD_DIR = "/tmp/uploads"
    OUTPUT_DIR = "/tmp/outputs"
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
    OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates/solar_template.xlsx")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

extractor = BillExtractor()
excel_handler = ExcelHandler(TEMPLATE_PATH)

@app.post("/upload")
async def upload_bill(file: UploadFile = File(...)):
    # 1. Save uploaded file
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    input_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")
    
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Extract data using AI
    mime_type = file.content_type
    extracted_data = await extractor.extract_data(input_path, mime_type)
    
    if not extracted_data:
        raise HTTPException(status_code=500, detail="Failed to extract data from bill")

    # 3. Fill Excel template
    output_filename = f"solar_calc_{file_id}.xlsx"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    try:
        excel_handler.fill_template(extracted_data, output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excel filling failed: {str(e)}")

    return {
        "file_id": file_id,
        "extracted_data": extracted_data,
        "download_url": f"/download/{output_filename}"
    }

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path, 
        filename=f"Solar_Load_Calculation.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
