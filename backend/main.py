from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from PIL import Image
import io
from medical_llm.medical_reporter import MedicalReportGenerator
from dermascope_model.classifier import classify_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def read_root():
    return {"message": "We are up!!"}

@app.post("/diagnose")
async def generate_information_report(
    age: str = Form(...),
    gender: str = Form(...),
    history: str = Form(...),
    symptoms: str = Form(...),
    lesion_location: str = Form(...),
    image: UploadFile = File(...),
    max_tokens: int = Form(600)
):
    contents = await image.read()
    image = Image.open(io.BytesIO(contents))

    ReportGenerator = MedicalReportGenerator()

    image_prediction = classify_image(image)

    return ReportGenerator.generate_report(age, gender, history, symptoms, image_prediction, lesion_location)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 