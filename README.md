# Solar Load Calculator (AI-Powered)

An automated system to extract electricity bill data using Gemini 1.5 Flash and fill a solar calculation Excel template.

## Features
- **AI Extraction:** Native multi-modal processing (PDF/Images) using Gemini 1.5 Flash.
- **Excel Automation:** Fills input cells while preserving formulas and formatting using `openpyxl`.
- **Premium UI:** Modern, responsive React dashboard with glassmorphism design.
- **End-to-End Flow:** Upload Bill → AI Analysis → Structured JSON → Excel Download.

## Tech Stack
- **Backend:** FastAPI (Python)
- **AI:** Google Generative AI (Gemini API)
- **Excel:** openpyxl
- **Frontend:** React, Tailwind CSS, Framer Motion, Lucide React

## Setup Instructions

### 1. Backend Setup
1. Navigate to `backend/`
2. Create a `.env` file and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Start the server:
   ```bash
   python3 main.py
   ```

### 2. Frontend Setup
1. Navigate to `frontend/`
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```

## Demo Submission Strategy
- **Accuracy:** The prompt is tuned for high-fidelity extraction from various utility bill formats.
- **Formulas:** The Excel logic preserves complex calculations (e.g., `Units / 120` for solar sizing).
- **UX:** The UI provides real-time feedback during the AI scanning process.
