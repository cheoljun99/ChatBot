#crud.py
# api.py에서 사용할 함수들에 대해서 정의 
# 데이터베이스에 작업을 수행하기 위한 CRUD (Create, Read, Update, Delete) 함수들을 정의
# SQLAlchemy ORM을 사용하여 데이터베이스와 상호작용하며, 데이터 삽입, 조회, 업데이트, 삭제 작업을 수행
import hashlib
import json
from sqlalchemy.orm import Session
import logging
from sqlalchemy.exc import SQLAlchemyError

from models import Access_Table,User,IoC,BoBwiki
from schema import Optional, Access_Data, IoC_Data, BoBwiki_Data
from config import conf

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_user_in_db(user_id: str, db: Session)-> bool:
    #user 테이블에서 데이터를 찾는 함수
    return db.query(User).filter(User.user_id == user_id).one_or_none() !=None

def write_access_data_in_db(access_id: str, access_item: Access_Data, db: Session)-> bool:
    #접근 시 access 테이블에 기록을 저장하는 함수
    try:
        access_table = Access_Table(
            user_id = access_item.user_id,
            channel_id = access_item.channel_id,
            access_id = access_id,
            access_time = access_item.access_time,
        )
        db.add(access_table)
        db.commit()
        logging.info(f"Access data for user {access_item.user_id} saved successfully.") #디비 저장성공
        return True
    except SQLAlchemyError as e:
        db.rollback()  # 트랜잭션 롤백
        logging.error(f"Error saving access data for user {access_item.user_id}: {str(e)}") # 디비 저장실패
        return False
    
def get_ioc_data_in_db(db: Session)-> Optional[IoC_Data]:
    #ioc테이블에서 데이터를 가져오는 함수
    try:
        ioc_List=db.query(IoC).filter().all()
        logging.info("IoC_Data retrieved successfully.") # IoC 테이블에서 데이터 가져오는 작동 성공
        if ioc_List:
            return [IoC_Data.model_validate(ioc) for ioc in ioc_List] # JSON으로 표현하기 위한 SQLAlchemy ORM 객체를 Pydantic 모델로 변환하는 과정
        return None
    except SQLAlchemyError as e:
        #db.rollback()  # 조회는 트랜잭션 롤백이 필요없음
        logging.error(f"Error retrieving IoC_Data: {str(e)}") # IoC 테이블에서 데이터 가져오는 작동 성공
        return None

def get_bobwiki_data_in_db(name:str,db: Session)-> Optional[BoBwiki_Data]:
    #BoBwiki 테이블에서 데이터를 가져오는 함수
    try:
        bobwiki=db.query(BoBwiki).filter(BoBwiki.name == name).one_or_none()
        logging.info("BoBwiki_Data retrieved successfully.") # BoBwiki 테이블에서 데이터 가져오는 작동 성공
        return bobwiki
    except SQLAlchemyError as e:
        #db.rollback()  # 조회는 트랜잭션 롤백이 필요없음
        logging.error(f"Error retrieving BoBwiki_Data: {str(e)}") # BoBwiki 테이블에서 데이터 가져오는 작동 성공
        return None