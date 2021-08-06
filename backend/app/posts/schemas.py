from tortoise.contrib.pydantic import pydantic_model_creator

from .models import Post

Post_Pydantic = pydantic_model_creator(Post, name="Post")
PostInWithProfileId_Pydantic = pydantic_model_creator(Post, name="PostInWithProfileId", include=("title", "body", "profile_id"))
PostIn_Pydantic = pydantic_model_creator(Post, name="PostIn", exclude_readonly=True)
