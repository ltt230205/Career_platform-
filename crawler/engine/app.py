from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import uuid
import os
import json

from crawler import SeleniumCrawler

app = FastAPI()

OUTPUT_DIR = "output"
TEMP_DIR = "temp"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


# ==============================
# 1. Crawl bằng file path
# ==============================
@app.post("/crawl/file")
def crawl_from_file(json_path: str):
    try:
        result = SeleniumCrawler.run_category(json_path)
        return {
            "status": "success",
            "message": "Crawl completed",
            "output": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ==============================
# 2. Crawl bằng JSON body
# ==============================
@app.post("/crawl/json")
def crawl_from_json(request: dict):
    temp_file = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.json")

    with open(temp_file, "w", encoding="utf-8") as f:   
        json.dump(request, f, ensure_ascii=False, indent=4)

    result = SeleniumCrawler.run_category(temp_file)

    return {
        "status": "success",
        "message": "Crawl completed",
        "output": result
    }