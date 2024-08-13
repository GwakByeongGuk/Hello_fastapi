from typing import List, Optional
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

# 성적 추가
@app.post('/sj', response_model=SungjukModel)
def sjadd(sj: SungjukModel, db: Session = Depends(get_db)):
    sj = Sungjuk(**dict(sj)) # 클라이언트가 전송한 성적데이터가
                             # pydantic으로 유효성 검사 후
                             # 데이터베이스에 저장할 수 있도록
                             # sqlalchemy 객체로 변환
    # py : Sungjuk(name=?, kor=?, eng=?, mat=?)
    # sa : Sungjuk(sj['name'], sj['kor'], sj['eng'], sj['mat'])

    db.add(sj)
    db.commit()
    db.refresh(sj)
    return sj

# 성적 상세 조회 - 학생번호로 조회
@app.get('/sj/{sjng}', response_model=Optional[SungjukModel])
def readone_sj(sjng: int, db: Session = Depends(get_db)):
    sungjuk = db.query(Sungjuk).filter(Sungjuk.sjng == sjng).first()
    return sungjuk

# 성적 삭제 - 학생번호로 조회
# 먼저, 삭제할 학생 데이터가 있는지 확인한 후 삭제 실행
@app.delete('/sj/{sjng}', response_model=Optional[SungjukModel])
def delete_sj(sjng: int, db: Session = Depends(get_db)):
    sungjuk = db.query(Sungjuk).filter(Sungjuk.sjng == sjng).first()
    if sungjuk:
        db.delete(sungjuk)
        db.commit()
    return sungjuk

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('sqlalchemy01:app', reload=True)
