from pydantic import BaseModel, Field
from datetime import datetime, timezone

class MessageLogBase(BaseModel):
    MessageId: int
    Model: str
    PromptTokens: int
    CompletionTokens: int
    TotalTokens: int
    TotalCost: float
    ResponseTime: float
    HasError: bool
    CreateDate: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MessageLogCreate(MessageLogBase):
    pass

class MessageLog(MessageLogBase):
    Id: int

    class Config:
        from_attributes = True
