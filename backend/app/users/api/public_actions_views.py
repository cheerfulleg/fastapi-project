from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Path
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate
from starlette import status
from starlette.responses import JSONResponse

from backend.app.auth.permissions import has_profile
from backend.app.posts.models import Post
from backend.app.posts.schemas import Post_Pydantic
from backend.app.users.models import Profile
from backend.app.users.schemas import Profile_Pydantic

public_actions_router = APIRouter()


@public_actions_router.post("/subscribe/{profile_id}")
async def subscribe(profile_id: int = Path(..., gt=0), current_profile: Profile = Depends(has_profile)):
    """
    **Has_Profile permissions required**

    Subscribe to another profile by id
    """
    profile_obj = await Profile.get(id=profile_id)
    subscribed = await profile_obj.subscribers.filter(id=current_profile.id)
    if subscribed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Already subscribed")
    await profile_obj.subscribers.add(current_profile)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Subscribed successfully"})


@public_actions_router.delete("/unsubscribe/{profile_id}")
async def subscribe(profile_id: int = Path(..., gt=0), current_profile: Profile = Depends(has_profile)):
    """
    **Has_Profile permissions required**

    Unsubscribe from another profile by id
    """
    profile_obj = await Profile.get(id=profile_id)
    subscribed = await profile_obj.subscribers.filter(id=current_profile.id)
    if not subscribed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not subscribed yet")
    await profile_obj.subscribers.remove(current_profile)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Unsubscribed successfully"})


@public_actions_router.get("/feed", response_model=Page[Post_Pydantic])
async def subscribe(current_profile: Profile = Depends(has_profile)):
    """
    **Has_Profile permissions required**

    Gets list of subscribed profiles posts
    """
    subs = await current_profile.filter(subscribers=current_profile.id)
    ids = [sub.id for sub in subs]
    return await paginate(Post.filter(profile_id__in=ids))
