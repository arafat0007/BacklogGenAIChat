from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Chat(Base):
    __tablename__ = "Chat"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    User = Column(String(255))
    CreateDate = Column(DateTime, default=datetime.now)