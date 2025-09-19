from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

# 모든 도메인에서 호출 가능
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "백엔드 연결 확인 완료! 🎉"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    label = "고양이" if np.random.rand() > 0.5 else "강아지"
    class_index = 0 if label == "고양이" else 1
    confidence = float(np.random.rand() * 0.5 + 0.5)

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
