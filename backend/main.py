from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from PIL import Image
import io
from medical_llm.medical_reporter import MedicalReportGenerator
from dermascope_model.classifier import classify_image, classify_image_with_confidence

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

@app.post("/classify")
async def classify_endpoint(
    image: UploadFile = File(...)
):
    contents = await image.read()
    image = Image.open(io.BytesIO(contents))
    ReportGenerator = MedicalReportGenerator()

    class_labels = {
        "actinic keratosis": "A rough, scaly patch on the skin caused by years of sun exposure, potentially precancerous.",
        "basal cell carcinoma": "The most common type of skin cancer, appearing as a pearly or waxy bump, often on sun-exposed areas.",
        "benign keratosis-like lesions": "Non-cancerous skin growths such as seborrheic keratoses and solar lentigines.",
        "dermatofibroma": "A benign, firm skin nodule, commonly appearing on the lower legs, often due to minor injury.",
        "melanoma": "A serious and aggressive form of skin cancer that originates in melanocytes; early detection is critical.",
        "melanocytic nevi": "Common moles that are generally harmless but should be monitored for changes in shape or color.",
        "vascular lesions": "Abnormal blood vessel growths, including hemangiomas and pyogenic granulomas, often appearing red or purple."
    }


    prediction = classify_image_with_confidence(image)
    prediction["Meaning"] = class_labels[prediction["Prediction"].lower()]

    return prediction

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)