from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 모든 도메인에서 호출 가능
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 연결 테스트용 메시지
@app.get("/")
def root():
    return {"message": "백엔드 연결 확인용 테스트 서버"}

# 이미지 업로드 테스트
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "size_bytes": len(contents)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
