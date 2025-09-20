from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Allow Streamlit frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

def evaluate_omr_image(image_bytes, version="version1"):
    """
    Simplified OMR evaluation logic:
    Detect filled bubbles using thresholding and contours.
    """
    # Convert bytes to OpenCV image
    file_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur and threshold
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Placeholder: simple scoring
    total_questions = 100  # 5 subjects * 20
    filled_count = min(len(contours), total_questions)  # avoid overflow

    # Split scores into 5 subjects
    scores = {}
    per_subject = 20
    subjects = ["subject1","subject2","subject3","subject4","subject5"]
    start = 0
    for i, sub in enumerate(subjects):
        end = start + per_subject
        score = min(filled_count - start, per_subject)
        if score < 0: score = 0
        scores[sub] = score
        start = end

    total_score = sum(scores.values())

    return scores, total_score

@app.post("/evaluate/")
async def evaluate_omr(file: UploadFile = File(...), version: str = Form(...)):
    # Read image bytes
    image_bytes = await file.read()
    scores, total = evaluate_omr_image(image_bytes, version)

    return {
        "filename": file.filename,
        "version": version,
        "scores": scores,
        "total": total
    }
