from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 모든 도메인에서 호출 가능
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 브라우저에서 바로 확인 가능
@app.get("/")
def root():
    return {
        "message": "백엔드 연결 확인 완료! 🎉",
        "info": "GitHub Pages에서 접속해도 이 메시지가 보입니다."
    }

# 이미지 업로드 테스트용 (선택)
@app.post("/predict")
async def predict(file: bytes = b""):
    return {
        "message": "POST 요청도 정상 작동",
        "filename": getattr(file, "filename", "테스트 이미지 없음"),
        "size_bytes": len(file)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
