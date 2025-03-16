from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from services.planetnet_classification import classify_plant
from services.chat_gpt_flower_info import get_plant_info

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
async def classify_plant_endpoint(file: UploadFile = File(...)):
    image_bytes = await file.read()
    scientific_name = classify_plant(image_bytes, file.filename, file.content_type)
    plant_details = get_plant_info(scientific_name)
    return plant_details


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
