from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from backend.app.users.models import Profile, User

Profile_Pydantic = pydantic_model_creator(Profile, name="Profile", exclude=("user_id",))
ProfileIn_Pydantic = pydantic_model_creator(Profile, name="ProfileIn", exclude_readonly=True, exclude=("avatar_url",))
ProfileInWithUserId_Pydantic = pydantic_model_creator(
    Profile,
    name="ProfileInWithUserId",
    include=("user_id", "first_name", "last_name", "date_of_birth"),
)

User_Pydantic = pydantic_model_creator(User, name="User", exclude=("password_hash",))
UserDefaultIn_Pydantic = pydantic_model_creator(User, name="UserDefaultIn", exclude=("is_admin",), exclude_readonly=True)
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
UserInNoPassword_Pydantic = pydantic_model_creator(User, name="UserInNoPassword", exclude=("password_hash",), exclude_readonly=True)


class ResetPassword(BaseModel):
    password: str
