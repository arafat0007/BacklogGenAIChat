from pydantic import BaseModel

class DatastoreBase(BaseModel):
    Keywords: str
    Title: str
    Source: str
    Content: str
    Category: str
    IsUserForEmbedding: bool

class DatastoreCreate(DatastoreBase):
    pass

class Datastore(DatastoreBase):
    Id: int

    class Config:
        from_attributes = True
