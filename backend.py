from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import numpy as np
import uvicorn

app = FastAPI()

# GitHub Pages에서 호출 가능하게 CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 이미지 읽기
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    width, height = img.size

    # 테스트용 랜덤 결과
    label = "고양이" if np.random.rand() > 0.5 else "강아지"
    class_index = 0 if label == "고양이" else 1
    confidence = float(np.random.rand() * 0.5 + 0.5)  # 0.5 ~ 1.0

    return {
        "label": label,
        "class_index": class_index,
        "confidence": confidence,
        "filename": file.filename,
        "size": len(contents),
        "width": width,
        "height": height
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
