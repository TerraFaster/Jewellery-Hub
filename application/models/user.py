from datetime import datetime, timedelta

from fastapi import Request
from tortoise import fields
from tortoise.models import Model
from jose import jwt, JWTError

from application import config
from application.enums import Currency

from application.models.market import MarketItem


class User(Model):
    id = fields.BigIntField(pk=True, generated=False)
    username = fields.CharField(max_length=24, unique=True)
    email = fields.CharField(max_length=48, unique=True)
    password = fields.CharField(max_length=64)
    currency = fields.CharField(max_length=6, default=Currency.uah)
    created_at = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)
    cart = fields.JSONField(default=[])

    def __str__(self):
        return f"<User username={self.username} id={self.id}>"

    class Meta:
        table = "users"

    def generate_access_token(self, expires_delta: timedelta = None) -> str:
        expires = datetime.utcnow() + (expires_delta or timedelta(weeks=1))
        data = {"sub": str(self.id), "exp": expires}

        encoded_jwt = jwt.encode(
            data, 
            config.JWT_SECRET_KEY, 
            algorithm=config.JWT_ALGORITHM
        )

        return encoded_jwt

    @classmethod
    async def from_access_token(cls, token: str):
        if not token:
            return None

        try:
            payload = jwt.decode(
                token, 
                config.JWT_SECRET_KEY, 
                algorithms=config.JWT_ALGORITHM
            )

        except JWTError:
            return None

        else:
            user = await User.get_or_none(id=payload.get("sub"))
            return user

    @classmethod
    async def dependency(cls, request: Request):
        token = request.cookies.get("Authorization")

        if token is None:
            token = request.headers.get("Authorization")

        if token is None:
            return None

        user = await cls.from_access_token(token)
        return user

    async def get_cart_items(self) -> list[MarketItem]:
        items = []
        has_deleted_items = False

        for item_id in self.cart:
            item = await MarketItem.get_or_none(id=item_id)

            if item is None:
                self.cart.remove(item_id)
                continue

            items.append(item)

        if has_deleted_items:
            await self.save()

        return items
