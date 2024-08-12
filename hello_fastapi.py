from fastapi import FastAPI

# fastapi 앱 실행 방버
# python -m uvicorn 파일명:app --reload
# python -m uvicorn hello_fastapi:app --reload
app = FastAPI()

@app.get('/')
def index():
    return 'Hello World!!'