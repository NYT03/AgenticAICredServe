from fastapi import FastAPI, UploadFile, File
import shutil
import os
from .extractor import process_document
from .collection_agent import run_agent

app = FastAPI()

UPLOAD_FOLDER = "samples"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = process_document(file_path)
    return result

@app.get("/run-agent")
def run_collection_agent():
    result = run_agent()
    return result