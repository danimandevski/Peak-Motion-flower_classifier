# services/planet_classification.py
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()

# Plant classification API configuration
API_KEY = '2b10mD9ZagycYz5vQn0or5viQ'
API_URL = (
    "https://my-api.plantnet.org/v2/identify/all?"
    "include-related-images=false&no-reject=false&nb-results=1&lang=en&api-key=" + API_KEY
)
HEADERS = {"accept": "application/json"}

def classify_plant(image_bytes: bytes, filename: str, content_type: str) -> str:
    files = {"images": (filename, image_bytes, content_type)}
    try:
        response = requests.post(API_URL, headers=HEADERS, files=files)
        response.raise_for_status()
        result = response.json()
        # Assume that the API returns a key 'bestMatch' holding the scientific name
        scientific_name = result.get("bestMatch", "No match found")
        return scientific_name
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error calling plant classification API: {str(e)}")
