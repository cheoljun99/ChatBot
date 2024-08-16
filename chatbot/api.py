#api.py
# 프론트의 요청을 식별하고 요청에 대한 데이터를 처리함
# FastAPI를 사용하여 API 엔드포인트를 정의하고, HTTP 요청을 처리함
# 엔드포인트는 CRUD 함수와 연동되어 데이터베이스 작업을 수행함

import hashlib
from fastapi import FastAPI, Depends, HTTPException
import logging
from sqlalchemy.orm import Session
from database import db
from schema import Access_Data
from crud import write_access_data_in_db,check_user_in_db,get_ioc_data_in_db
from fastapi.encoders import jsonable_encoder


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

@app.get("/cheoljun99")
async def root():
    return {"message": "BoB 13기 제품개발트랙 박철준입니다. BoB 13기 제품개발트랙 화이팅!"}

@app.post("/access")
async def access(access_item: Access_Data, access_db: Session = Depends(db.get_session)):
    logging.info("api의 access 메소드 접근")
    checker = check_user_in_db(access_item.user_id, access_db)
    if not checker :
        raise HTTPException(status_code=403, detail="접근이 거부되었습니다.")
    #logging.info(checker)
    
    # access_id 생성
    access_string = f"{access_item.access_time}{access_item.channel_id}{access_item.user_id}"
    access_id = hashlib.sha256(access_string.encode()).hexdigest()
    #logging.info(access_id)

    errorHandler = write_access_data_in_db(access_id,access_item, access_db)
    if not errorHandler:
        raise HTTPException(status_code=500, detail="데이터베이스에 접근 데이터를 저장하는 동안 오류가 발생했습니다.")
    
    return {"message": f"환영합니다!"}


@app.get("/ioc")
async def ioc(db: Session = Depends(db.get_session)):
    ioc_data = get_ioc_data_in_db(db)
    if ioc_data is None:
        raise HTTPException(status_code=404, detail="IoC 데이터가 존재하지 않습니다.")
    
    return jsonable_encoder(ioc_data)

