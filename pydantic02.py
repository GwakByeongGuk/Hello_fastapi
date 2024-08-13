from datetime import datetime
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

# 회원 정보 모델 정의
class CRUD(BaseModel):
    userid: str
    passwd: str
    name: str
    email: str
    regdate: datetime

# 회원 정보 저장용 변수
CRUD_db: List[CRUD] = []
app = FastAPI()

# 모든 회원 정보 조회
@app.get('/crud', response_model=List[CRUD])
def crud_readall():
    return CRUD_db

# 새로운 회원 정보 생성
@app.get('/crudadd', response_model=CRUD)
def crud_create():
    crud = CRUD(userid='123456', passwd='654321', name='병국',
                email='teereal@naver.com', regdate=datetime.now().replace(microsecond=0))
    CRUD_db.append(crud)
    return crud

# 특정 회원 정보 조회 - userid로 조회
@app.get('/crudone/{userid}', response_model=CRUD)
def crudone(userid: str):
    findone = CRUD(userid='None', passwd='None', name='None',
                   email='None', regdate=datetime.now().replace(microsecond=0))
    for crud in CRUD_db:
        if crud.userid == userid:
            findone = crud
    return findone

# 회원 정보 삭제 - userid로 삭제
@app.delete('/crudrmv/{userid}', response_model=CRUD)
def crudrmv(userid: str):
    rmvone = CRUD(userid='None', passwd='None', name='None',
                  email='None', repregdate=datetime.now().replace(microsecond=0))
    for idx, crud in enumerate(CRUD_db):
        if crud.userid == userid:
            rmvone = CRUD_db.pop(idx)
            break
    return rmvone

# 회원 정보 수정 - userid로 조회 후 수정
@app.put('/crud', response_model=CRUD)
def crudput(one: CRUD):
    putone = CRUD(userid='None', passwd='None', name='None',
                  email='None', regdate=datetime.now().replace(microsecond=0))
    for idx, crud in enumerate(CRUD_db):
        if crud.userid == one.userid:
            CRUD_db[idx] = one
            putone = one
            break
    return putone

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('pydantic02:app', reload=True)
