#schema.py
#프론트로 받은 데이터 혹은 보낼 데이터의 형식을 지정해줌

from typing import Optional
from pydantic import BaseModel # pylint: disable=no-name-in-module
from datetime import datetime

class Access_Data(BaseModel):
    user_id: Optional[str] = None
    channel_id:Optional[str] =None
    access_time:Optional[datetime]
    access_id:Optional[str]=None
    class Config:
        orm_mode=True
        
class User_Data(BaseModel):
    user_id: Optional[str] = None
    class Config:
        orm_mode=True

class IoC_Data(BaseModel):
    column_a: Optional[str] = None
    column_b: Optional[str] = None
    column_c: Optional[str] = None
    class Config:
        orm_mode=True
        from_attributes = True # Pydantic v2 설정
        # SQLAlchemy ORM 객체를 FastAPI 응답으로 바로 반환하려면,
        # FastAPI가 해당 객체를 JSON으로 직렬화할 수 있어야 한다.
        # 하지만 SQLAlchemy ORM 객체는 바로 JSON으로 직렬화될 수 없기 때문에,
        # 이를 Pydantic 모델로 변환하여 JSON으로 직렬화 할 수 있다.
        # 이때 SQLAlchemy ORM 객체를 Pydantic 모델로 변환하는 과정을 가능하게 하는 설정이 from_attributes = True이다.

class BoBwiki_Data(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    info: Optional[str] = None
    class Config:
        orm_mode=True
        from_attributes = True # Pydantic v2 설정
