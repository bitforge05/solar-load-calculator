import json
import os
import httpx
import base64
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class BillExtractor:
    def __init__(self):
        # Using gemini-1.5-flash as the stable production model
        # The URL can be easily swapped if a different model is required
        self.model = "gemini-1.5-flash" 
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={GEMINI_API_KEY}"

    async def extract_data(self, file_path: str, mime_type: str):
        """
        Asynchronous extraction using httpx and the Gemini API.
        """
        with open(file_path, "rb") as f:
            base64_data = base64.b64encode(f.read()).decode('utf-8')

        payload = {
            "contents": [{
                "parts": [
                    {"text": "Extract Maharashtra MSEDCL bill data into JSON format with keys: consumer_number, consumer_name, billing_month, units_consumed, bill_amount, sanctioned_load, connected_load, tariff_type, meter_number, contract_demand. Output ONLY JSON."},
                    {"inline_data": {"mime_type": mime_type, "data": base64_data}}
                ]
            }]
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self.api_url, json=payload)
                response.raise_for_status()
                result = response.json()
                
                if "candidates" in result:
                    text = result["candidates"][0]["content"]["parts"][0]["text"]
                    # Clean up markdown if present
                    text = text.replace("```json", "").replace("```", "").strip()
                    return json.loads(text)
                else:
                    print(f"API Error: {result}")
                    return None
            except Exception as e:
                print(f"Error during extraction: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    print(f"Response status: {e.response.status_code}")
                    print(f"Response body: {e.response.text}")
                return None
