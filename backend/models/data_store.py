from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Datastore(Base):
    __tablename__ = "Datastore"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Keywords = Column(String(255))
    Title = Column(String(255))
    Source = Column(String(255))
    Content = Column(Text)
    Category = Column(String(255))
    IsUserForEmbedding = Column(Boolean, default=False)
