from passlib.handlers.bcrypt import bcrypt
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)
    is_admin = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now=True)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)


User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)


class Profile(Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField('models.User', related_name='profile', on_delete=fields.CASCADE)
    first_name = fields.CharField(60)
    last_name = fields.CharField(60)
    date_of_birth = fields.DateField()

    class PydanticMeta:
        exclude = ('id',)


Profile_Pydantic = pydantic_model_creator(Profile, name='Profile')
ProfileIn_Pydantic = pydantic_model_creator(Profile, name='ProfileIn')