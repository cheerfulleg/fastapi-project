from tortoise.contrib.pydantic import pydantic_model_creator

from .models import Post

Post_Pydantic = pydantic_model_creator(Post, name="Post")
PostIn_Pydantic = pydantic_model_creator(Post, name="PostIn", exclude_readonly=True)
