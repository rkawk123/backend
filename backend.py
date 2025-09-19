from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io
import os
import requests

app = FastAPI()

# CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 구글 드라이브 모델 파일
import gdown

FILE_ID = "1Java89-rJabP2jwLmQuRlYDYO8cvsWjA"
MODEL_PATH = "my_model.h5"
GDRIVE_URL = f"https://drive.google.com/uc?id={FILE_ID}"  # gdown 전용 URL

if not os.path.exists(MODEL_PATH):
    print("모델 다운로드 중...")
    gdown.download(GDRIVE_URL, MODEL_PATH, quiet=False)
    print("모델 다운로드 완료!")


# 모델 다운로드
if not os.path.exists(MODEL_PATH):
    print("모델 다운로드 중...")
    r = requests.get(GDRIVE_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(r.content)
    print("모델 다운로드 완료!")

# 모델 로드
model = load_model(MODEL_PATH)

# 클래스 이름 (모두 대문자)
CLASS_NAMES = [
    "ACRYLIC", "DENIM", "COTTON", "FUR", "LINEN", 
    "NYLON", "POLYESTER", "PUFFER", "RAYON", 
    "SLIK", "SPANDEX", "VELVET", "WOOL"
]

@app.get("/")
def root():
    return {"message": "백엔드 연결 확인 완료! 🎉"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    img = img.resize((224, 224))  # 모델 입력 크기에 맞추기
    x = np.array(img) / 255.0
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    class_index = int(np.argmax(preds))
    label = CLASS_NAMES[class_index]
    confidence = float(preds[0][class_index])

    return {
        "filename": file.filename,
        "size_bytes": len(contents),
        "label": label,
        "class_index": class_index,
        "confidence": confidence
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




