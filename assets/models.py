from sqlalchemy import Column,Integer,String,Boolean,DateTime,Date,Text
from assets.database import Base
from datetime import datetime as dt

class Users(Base):

    __tablename__ = "users"
    user_id = Column(String,primary_key=True)
    name = Column(String,unique=False)
    area_code = Column(String,unique=False,default='130000')
    del_flag = Column(Boolean,unique=False,default=False)

class Areas(Base):

    __tablename__ = "areas"
    area_code = Column(String,primary_key=True)
    prefecture_name = Column(String,unique=True)