import re

from passlib.handlers.bcrypt import bcrypt
from tortoise import Model, fields
from tortoise.exceptions import NoValuesFetched
from tortoise.validators import RegexValidator

from backend.app.posts.models import Post

REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


class User(Model):
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(50, unique=True, index=True)
    email = fields.CharField(120, validators=[RegexValidator(REGEX, re.I)])
    password_hash = fields.CharField(128)
    is_admin = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now=True)

    profile: fields.ReverseRelation["Profile"]

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)


class Profile(Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField("models.User", related_name="profile", on_delete=fields.CASCADE)
    first_name = fields.CharField(60)
    last_name = fields.CharField(60)
    date_of_birth = fields.DateField()
    subscribers = fields.ManyToManyField("models.Profile", through="subscriptions", on_delete=fields.CASCADE, null=True, required=False, forward_key="subscriber")
    avatar_url = fields.TextField(default=None, required=False, null=True)

    posts: fields.ReverseRelation["Post"]

    def user_id(self) -> int:
        return self.user.id

    def subscribers_count(self) -> int:
        try:
            return len(self.subscribers)
        except NoValuesFetched:
            return 0

    class PydanticMeta:
        computed = (
            "user_id",
            "subscribers_count",
        )
