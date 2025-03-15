import requests

API_KEY = '2b10mD9ZagycYz5vQn0or5viQ'
API_URL = (
        "https://my-api.plantnet.org/v2/identify/all?"
        "include-related-images=false&no-reject=false&nb-results=1&lang=en&api-key=" + API_KEY
)
HEADERS = {
    "accept": "application/json"
}


def classify_plant(image_bytes: bytes, filename: str, content_type: str) -> str:

    files = {"images": (filename, image_bytes, content_type)}

    response = requests.post(API_URL, headers=HEADERS, files=files)
    result = response.json()

    return result.get("bestMatch", "No match found")