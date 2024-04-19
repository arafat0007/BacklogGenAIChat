from pydantic import BaseModel, Field
from datetime import datetime, timezone

class FeedbackBase(BaseModel):
    ChatId: int
    Content: str
    Rating: int
    CreateDate: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    Id: int

    class Config:
        from_attributes = True
