from tortoise.contrib.pydantic import pydantic_model_creator

from .user import User
from .market import MarketItem, Category

User_Pydantic = pydantic_model_creator(User)
MarketItem_Pydantic = pydantic_model_creator(MarketItem)
