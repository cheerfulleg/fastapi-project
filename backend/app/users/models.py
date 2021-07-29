from passlib.handlers.bcrypt import bcrypt
from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)
    is_admin = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now=True)

    profile: fields.ReverseRelation["Profile"]

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)


class Profile(Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField('models.User', related_name='profile', on_delete=fields.CASCADE)
    first_name = fields.CharField(60)
    last_name = fields.CharField(60)
    date_of_birth = fields.DateField()

    def user_id(self) -> int:
        return self.user.id

    class PydanticMeta:
        computed = ('user_id',)
