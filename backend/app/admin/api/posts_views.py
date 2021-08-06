from fastapi import APIRouter, HTTPException
from fastapi.params import Path
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate
from starlette import status
from starlette.responses import JSONResponse

from backend.app.posts.models import Post
from backend.app.posts.schemas import Post_Pydantic, PostInWithProfileId_Pydantic
from backend.app.users.models import Profile

posts_router = APIRouter()


@posts_router.post("", status_code=201, response_model=Post_Pydantic)
async def create_post(post: PostInWithProfileId_Pydantic):
    """
    **Admin permissions required**

    Create post
    - **title**: post title, 120 characters
    - **body**:  post body, text field
    - **profile_id**: profile reference
    """
    post_obj = await Post.create(**post.dict(exclude_unset=True))
    return await Post_Pydantic.from_tortoise_orm(post_obj)


@posts_router.get("", response_model=Page[Post_Pydantic])
async def get_posts_list():
    """
    **Admin permissions required**

    Get list of existing posts
    """
    # posts = await Post_Pydantic.from_queryset(Post.all())
    return await paginate(Post)


@posts_router.get("/{post_id}", response_model=Post_Pydantic)
async def get_post_by_id(post_id: int = Path(..., gt=0)):
    """
    **Admin permissions required**

    Get post details
    """
    return Post_Pydantic.from_queryset_single(Post.get(id=post_id))


@posts_router.put("/{post_id}", response_model=Post_Pydantic)
async def update_post_by_id(post: PostInWithProfileId_Pydantic, post_id: int = Path(..., gt=0)):
    """
    **Admin permissions required**

    Update post
    - **title**: post title, 120 characters
    - **body**:  post body, text field
    - **profile_id**: profile reference
    """
    profile_obj = await Profile.get(id=post.dict().get("profile_id"))
    if not profile_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await Post.filter(id=post_id).update(**post.dict(exclude_unset=True))
    return await Post_Pydantic.from_queryset_single(Profile.get(id=post_id))


@posts_router.delete("/{post_id}")
async def delete_post_by_id(post_id: int = Path(..., gt=0)):
    """
    **Admin permissions required**

    Delete post
    """
    deleted_count = await Post.filter(id=post_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Profile not found")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Post deleted successfully"},
    )
