from pydantic import BaseModel, Field
from datetime import datetime, timezone

class MessageBase(BaseModel):
    ChatId: int
    Type: str
    Content: str
    CreateDate: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    Id: int

    class Config:
        from_attributes = True
