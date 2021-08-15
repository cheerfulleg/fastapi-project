from backend.app.chat.base_service import BaseService
from backend.config.settings import db


class ChatService(BaseService):
    collection = db.get_collection("chat_collection")


class MessageService(BaseService):
    collection = db.get_collection("message_collection")
