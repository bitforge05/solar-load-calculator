from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
import uuid
import sys

# We are in frontend/api/index.py, so services is in ../services
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from services.extractor import BillExtractor
from services.excel_handler import ExcelHandler

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage (Using /tmp for Vercel)
UPLOAD_DIR = "/tmp/uploads"
OUTPUT_DIR = "/tmp/outputs"
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "../templates/solar_template.xlsx")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

extractor = BillExtractor()
excel_handler = ExcelHandler(TEMPLATE_PATH)

@app.get("/api")
async def health():
    return {"status": "ok", "location": "frontend/api"}

@app.post("/api/upload")
async def upload_bill(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    input_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")
    
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    mime_type = file.content_type
    extracted_data = await extractor.extract_data(input_path, mime_type)
    
    if not extracted_data:
        raise HTTPException(status_code=500, detail="Failed to extract data")

    output_filename = f"solar_calc_{file_id}.xlsx"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    excel_handler.fill_template(extracted_data, output_path)

    return {
        "file_id": file_id,
        "extracted_data": extracted_data,
        "download_url": f"/api/download/{output_filename}"
    }

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename=filename)
