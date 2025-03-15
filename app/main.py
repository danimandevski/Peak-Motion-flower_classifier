from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from services.planetnet_classification import classify_plant

app = FastAPI()

origins = [
    "http://localhost:8100",
    "http://127.0.0.1:8100",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/classify")
async def classify_plant_endpoint(image: UploadFile = File(...)):
    image_bytes = await image.read()

    best_match = classify_plant(image_bytes, image.filename, image.content_type)

    return {"best_match": best_match}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
