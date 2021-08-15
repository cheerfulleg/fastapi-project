from typing import List

from pydantic import BaseModel

from backend.app.chat.mixins import TimestampMixin, MongoIdMixin


class ChatIn(BaseModel):
    members: List[int] = []


class ChatModel(ChatIn, TimestampMixin):
    pass


class ChatInDB(MongoIdMixin, ChatModel):
    class Config:
        schema_extra = {
            "example": {
                "_id": "6117e58bca76ccfda2b442b6",
                "members": [1, 2],
                "timestamp": "2021-08-14T15:47:23.120000",
            }
        }


class MessageIn(BaseModel):
    body: str


class MessageModel(TimestampMixin, MessageIn):
    chat_id: str
    user_id: int
    edited: bool = False


class MessageInDB(MongoIdMixin, MessageModel):
    class Config:
        schema_extra = {"example": {"_id": "6117e58bca76ccfda2b442b6", "chat_id": "6117e58bca76fffda2b442b6", "body": "Lorem ipsum...", "timestamp": "2021-08-14T15:47:23.120000"}}
