from sqlalchemy import Column, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Feedback(Base):
    __tablename__ = "Feedback"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    ChatId = Column(Integer)
    Content = Column(Text)
    Rating = Column(Integer)
    CreateDate = Column(DateTime, default=datetime.now)