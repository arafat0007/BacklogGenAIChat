from pydantic import BaseModel, Field
from datetime import datetime, timezone

class ChatBase(BaseModel):
    User: str
    CreateDate: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    Id: int

    class Config:
        from_attributes = True
