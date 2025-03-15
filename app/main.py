from fastapi import FastAPI, File, UploadFile
import uvicorn

from services.planetnet_classification import classify_plant

app = FastAPI()

@app.post("/classify")
async def classify_plant_endpoint(image: UploadFile = File(...)):
    image_bytes = await image.read()

    best_match = classify_plant(image_bytes, image.filename, image.content_type)

    return {best_match}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
