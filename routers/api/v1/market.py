import time

from fastapi import APIRouter, Depends, Form, responses

from application.models import User, MarketItem, MarketItem_Pydantic


router = APIRouter(prefix="/api/market", tags=["api", "market"])


class AddItemForm:
    def __init__(
        self, 
        title: str = Form(), 
        description: str = Form(), 
        price: int = Form(), 
        category_id: int = Form(), 
        tags: list[str] = Form()
    ) -> None:
        self.title = title
        self.description = description
        self.price = price
        self.category_id = category_id
        self.tags = tags


@router.post("/add-item")
async def add_item(
    user: User = Depends(User.dependency), 
    form: AddItemForm = Depends()
):
    if not user:
        return responses.JSONResponse({"error": "Unauthorized"}, 401)
    
    try:
        item = await MarketItem.create(
            id=int(time.time() * 10**8), 
            title=form.title, 
            description=form.description, 
            price=form.price, 
            category_id=form.category_id, 
            tags=form.tags
        )

        resp = responses.JSONResponse({
            "message": "success", 
            "item": (await MarketItem_Pydantic.from_tortoise_orm(item)).json()
        }, 200)

    except:
        resp = responses.JSONResponse({
            "error": "Unable to create item with provided data"
        }, 400)

    return resp
