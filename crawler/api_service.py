from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import json
import sys

# Thêm đường dẫn để nhận diện module engine
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from engine import crawler

app = FastAPI(title="TopCV Crawler API")

# Định nghĩa cấu trúc chuẩn theo file JSON của bạn
class Step(BaseModel):
    type: str
    args: Dict[str, Any]

class TopCVConfig(BaseModel):
    url: str        # Đường dẫn chromedriver
    repeat: int     # Số lần lặp (ví dụ: 5)
    url_web: str    # Link web (TopCV)
    steps: List[Step]

@app.post("/run-topcv")
async def run_topcv_job(config: TopCVConfig):
    try:
        # 1. Đảm bảo thư mục metadata và output tồn tại
        os.makedirs("metadata", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        # 2. Lưu file cấu hình vào metadata/topcv_category.json
        # Chúng ta dùng tên mặc định hoặc có thể lấy từ tham số nếu muốn
        json_path = os.path.join("metadata", "topcv_category.json")
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(config.dict(), f, indent=4, ensure_ascii=False)

        # 3. Tạo file job .py tương ứng để lưu vết
        job_script_path = "job_topcv_category.py"
        with open(job_script_path, "w", encoding="utf-8") as f:
            f.write(f"""
from engine import crawler
if __name__ == "__main__":
    result = crawler.run_category("{json_path}")
    print(result)
            """)

        # 4. Kích hoạt Crawler chạy trực tiếp
        # Hàm này sẽ chạy qua 5 lần lặp (repeat: 5), mỗi lần Click Next và Extract
        print(f"🚀 Đang bắt đầu cào dữ liệu: {config.url_web}")
        result = crawler.run_category(json_path)

        return {
            "status": "success",
            "message": "Đã thực hiện xong 5 lượt cào",
            "files_created": {
                "config": json_path,
                "script": job_script_path,
                "output_directory": "output/"
            },
            "data": result # Trả về dữ liệu cuối cùng gộp được
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)