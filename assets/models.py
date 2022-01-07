from sqlalchemy import Column,Integer,String,Boolean,DateTime,Date,Text
from assets.database import Base
from datetime import datetime as dt

class Users(Base):

    __tablename__ = "users"
    user_id = Column(String,primary_key=True)
    name = Column(String,unique=False)
    area_code = Column(String,unique=False)
    del_flag = Column(Boolean,unique=False,default=False)
