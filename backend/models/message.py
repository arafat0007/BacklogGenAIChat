from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = "Message"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    ChatId = Column(Integer)
    Type = Column(String(255))
    Content = Column(Text)
    CreateDate = Column(DateTime, default=datetime.now)
