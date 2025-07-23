from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import base64
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/enhance")
async def enhance_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    base64_image = "data:image/jpeg;base64," + base64.b64encode(image_bytes).decode()

    response = requests.post(
        "https://eugenesiow-real-esrgan.hf.space/run/predict",
        json={"data": [base64_image]},
        headers={"Content-Type": "application/json"}
    )

    result = response.json()
    enhanced_image_url = result["data"][0]

    return {"enhanced_url": enhanced_image_url}
