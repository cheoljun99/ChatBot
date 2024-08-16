#models.py
# 백엔드에서 객체를 데이터베이스에 넣기 위해 SQLAlchemy를 사용하여 데이터베이스의 테이블과 동일한 구조의 ORM 모델을 정의함
# ORM 모델은 데이터베이스 테이블의 컬럼과 매핑되며, 데이터를 삽입, 조회, 업데이트, 삭제하는 작업을 수행

from sqlalchemy import Column, DateTime, Integer, String 
from database import Base

class Access_Table(Base):
    __tablename__='access_table'

    id = Column(Integer,primary_key=True)
    user_id = Column(String)
    channel_id = Column(String)
    access_time = Column(DateTime)
    access_id = Column(String)

class User(Base):
    __tablename__='user'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, primary_key=True)

class IoC(Base):
    __tablename__='ioc'

    id = Column(Integer, primary_key=True)
    column_a = Column(String)
    column_b = Column(String)
    column_c = Column(String)

class BoBwiki(Base):
    __tablename__='BoBwiki'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    info = Column(String)