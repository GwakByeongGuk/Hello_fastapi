from typing import List
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# 데이터베이스 설정
sqlite_url = 'sqlite:///python.db'
engine = create_engine(sqlite_url, connect_args={'check_same_thread': False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델
Base = declarative_base()

class Sungjuk(Base):
    __tablename__ = 'sungjuk'

    sjng = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    kor = Column(Integer)
    eng = Column(Integer)
    mat = Column(Integer)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 데이터베이스 세션을 의존성으로 주입하기 위한 함수
def get_db():
    db = SessionLocal() # 데이터베이스 세션 객체 생성
    try:
        yield db # yield : 파이썬 제너레이터 객체
                 # 함수가 호출될 때 비로소 객체를 반환(넘김)
    finally:
        db.close() # 데이터베이스 세션 닫음 (db 연결해제, 리소스 반환)

# Pydantic 모델
class SungjukModel(BaseModel):
    sjng: int
    name: str
    kor: int
    eng: int
    mat: int

    class Config:
        orm_mode = True

# FastAPI 메인
app = FastAPI()

@app.get('/')
def index():
    return 'Hello, sqlalchemy!!'

# 성적 조회
# Depends : 의존성 주입 - db 세션 제공
# => 코드 재사용성 향상, 관리 용이성 향상
@app.get('/sj', response_model=List[SungjukModel])
def read_sj(db: Session = Depends(get_db)):
    sungjuks = db.query(Sungjuk).all()
    return sungjuks

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('sqlalchemy01:app', reload=True)
