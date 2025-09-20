from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
from omr_evaluator import evaluate_omr_sheet

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "OMR Evaluation API is running"}

@app.post("/evaluate_omr/")
async def evaluate_omr(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Example answer key, adjust as per your sheet
    answer_key = {i: 'A' for i in range(1, 101)}
    result = evaluate_omr_sheet(file_location, answer_key)
    return result
