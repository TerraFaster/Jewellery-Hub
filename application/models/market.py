from tortoise import fields
from tortoise.models import Model


class Category(Model):
    title = fields.CharField(max_length=16)


class MarketItem(Model):
    id = fields.BigIntField(pk=True, generated=False)
    title = fields.CharField(max_length=64)
    description = fields.TextField()
    price = fields.IntField()
    images = fields.JSONField(default=[])
    category = fields.ForeignKeyField("models.Category")
    tags = fields.JSONField(default=[])
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "market_items"
