from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from starlette.responses import JSONResponse

from ..models import Post
from ..schemas import Post_Pydantic, PostIn_Pydantic
from ...auth.permissions import has_profile
from ...users.models import Profile

posts_router = APIRouter()


@posts_router.post('', status_code=201, response_model=Post_Pydantic)
async def create_post(post: PostIn_Pydantic, profile: Profile = Depends(has_profile)):
    """
    **Has_Profile permissions required**

    Create post
    - **title**: post title, 120 characters
    - **body**:  post body, text field
    """
    post_obj = await Post.create(**post.dict(exclude_unset=True), profile_id=profile.id)
    return await Post_Pydantic.from_tortoise_orm(post_obj)


@posts_router.get('', response_model=List[Post_Pydantic])
async def get_profile_posts(profile: Profile = Depends(has_profile)):
    """
    **Has_Profile permissions required**

    Get list of current user's posts
    """
    return await Post_Pydantic.from_queryset(Post.filter(profile_id=profile.id))


@posts_router.get('/{post_id}', response_model=Post_Pydantic)
async def get_post_details(post_id: int = Path(..., gt=0), profile: Profile = Depends(has_profile)):
    """
    **Has_Profile permissions required**

    Get post details
    """
    return await Post_Pydantic.from_queryset_single(Post.get(id=post_id))


@posts_router.put('/{post_id}', response_model=Post_Pydantic)
async def update_post_by_id(post: PostIn_Pydantic, post_id: int = Path(..., gt=0),
                            profile: Profile = Depends(has_profile)):
    """
    **Has_Profile permissions required**

    Update post details:
    - **title**: post title, 120 characters
    - **body**:  post body, text field
    """
    post_obj = await Post.get(id=post_id)
    if not post_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await Post.filter(id=post_id).update(**post.dict(exclude_unset=True))
    return await Post_Pydantic.from_queryset_single(Post.get(id=post_id))


@posts_router.delete('/{post_id}')
async def delete_post_by_id(post_id: int = Path(..., gt=0), profile: Profile = Depends(has_profile)):
    """
    **Has_Profile permissions required**

    Delete post
    """
    deleted_count = await Post.filter(id=post_id)
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f'Post not found')
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Post deleted successfully'})
