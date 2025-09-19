from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 모든 도메인에서 호출 가능하게 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "백엔드 연결 확인용 테스트 서버"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 파일 이름과 크기만 반환
    contents = await file.read()
    return {
        "filename": file.filename,
        "size_bytes": len(contents)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

