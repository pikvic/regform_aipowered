from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    fio = Column(String)
    email = Column(String, unique=True)
    telegram = Column(String)
    vk = Column(String)