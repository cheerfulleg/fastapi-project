from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from starlette.responses import JSONResponse

from ..schemas import ChatInDB, ChatModel, MessageInDB, MessageIn, MessageModel
from ..services import ChatService, MessageService
from ...auth.permissions import has_profile
from ...users.models import Profile

chat_router = APIRouter()


@chat_router.get("", response_model=List[ChatInDB])
async def get_profile_chats(profile: Profile = Depends(has_profile)):
    """
    **Has_Profile permission required

    Get list of current user's chats
    """
    return await ChatService.filter({"members": profile.id})


@chat_router.get("/{profile_id}", response_model=ChatInDB)
async def get_chat_by_profile_id(profile_id: int = Path(..., gt=0), profile: Profile = Depends(has_profile)):
    """
    **Has_Profile permission required**

    Get chat by profile id, create one if not existed before
    """
    profile_obj = await Profile.get(id=profile_id)
    if not profile_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    members = [profile.id, profile_id]
    return await ChatService.get_or_create({"members": {"$all": members}}, default=ChatModel(members=members).dict())


@chat_router.get("/{chat_id}/messages", response_model=List[MessageInDB])
async def get_chat_messages(chat_id: str, profile: Profile = Depends(has_profile)):
    """
    **Has_Profile permission required**

    Get all messages in chat
    """
    chat_obj = await ChatService.get({"_id": ObjectId(chat_id)})
    if not chat_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return await MessageService.filter({"chat_id": chat_id})


@chat_router.post("/{chat_id}/messages", response_model=MessageInDB)
async def send_message(chat_id: str, message_body: MessageIn, profile: Profile = Depends(has_profile)):
    """
    **Has_Profile permission required**

    Send message to chat
    """
    message = MessageModel(**message_body.dict(), chat_id=chat_id, user_id=profile.id)
    return await MessageService.create(message.dict())


@chat_router.put("/{chat_id}/messages/{message_id}", response_model=MessageInDB)
async def edit_message(chat_id: str, message_id: str, message_body: MessageIn, profile: Profile = Depends(has_profile)):
    """
    **Has_Profile permission required**

    Update message
    """
    message_obj = await MessageService.get({"_id": ObjectId(message_id), "chat_id": chat_id})
    if not message_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    message = MessageModel(**message_body.dict(), chat_id=chat_id, user_id=profile.id, edited=True)
    return await MessageService.update({"_id": ObjectId(message_id)}, message.dict())


@chat_router.delete("/{chat_id}/messages/{message_id}")
async def delete_message(chat_id: str, message_id: str, profile: Profile = Depends(has_profile)):
    """
    **Has_Profile permission required**

    Delete message
    """
    deleted = await MessageService.delete({"_id": ObjectId(message_id), "chat_id": chat_id})
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Message deleted successfully"})
