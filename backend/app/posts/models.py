from tortoise import Model, fields


class TimestampMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class Post(Model, TimestampMixin):
    id = fields.IntField(pk=True)
    profile = fields.ForeignKeyField("models.Profile", related_name="posts", on_delete=fields.CASCADE)
    title = fields.CharField(120)
    body = fields.TextField()

    class Meta:
        order_by = ("-created_at",)
