from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MessageLog(Base):
    __tablename__ = "MessageLog"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    MessageId = Column(Integer)
    Model = Column(String(255))
    PromptTokens = Column(Integer)
    CompletionTokens = Column(Integer)
    TotalTokens = Column(Integer)
    TotalCost = Column(DECIMAL(10, 5))
    ResponseTime = Column(DECIMAL(10, 5))
    HasError = Column(Boolean)
    CreateDate = Column(DateTime, default=datetime.now)
