import re

from fastapi import APIRouter, Depends, Request, responses

from application import config
from application.models import User, MarketItem, MarketItem_Pydantic, Category


router = APIRouter(prefix="", tags=["index"])


@router.get("/")
async def index(request: Request, user: User = Depends(User.dependency)):
    last_market_items = await MarketItem.all().order_by("-created_at").limit(10)
    cart_items = await user.get_cart_items() if user else []
    categories = await Category.all()

    response = config.templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "user": user, 
            "last_market_items": last_market_items, 
            "cart_items": cart_items, 
            "categories": categories
        }
    )

    return response


@router.get("/search")
async def search(
    request: Request, 
    query: str = None, 
    tags: str = "", 
    user: User = Depends(User.dependency)
):
    if not query and not tags:
        return responses.RedirectResponse("/", status_code=302)

    tags = tags.split(" ")
    search_by_tags = bool(tags)

    items = await MarketItem.all()

    matching_items = []
    search_words = re.findall(r"\b\w+\b", query.lower())

    for item in items:
        item_text = f"{item.title} {item.description} {' '.join(item.tags)}".lower()
        match_score = 0

        if search_by_tags:
            for tag in tags:
                if tag in item.tags:
                    match_score += 1

        for word in search_words:
            if word in item_text:
                match_score += 1

        if match_score > 0:
            matching_items.append((item, match_score))

    matching_items.sort(key=lambda x: x[1], reverse=True)

    items = [item[0] for item in matching_items]
    cart_items = await user.get_cart_items() if user else []
    categories = await Category.all()

    response = config.templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "user": user, 
            "item_blocks": {
                query.title(): items
            }, 
            "cart_items": cart_items, 
            "categories": categories
        }
    )

    return response


@router.get("/category/{category_id}")
async def category(
    request: Request, 
    category_id: int, 
    user: User = Depends(User.dependency)
):
    category = await Category.get_or_none(id=category_id)

    if category is None:
        return responses.RedirectResponse("/", status_code=302)

    items = await MarketItem.filter(category_id=category_id)
    cart_items = await user.get_cart_items() if user else []
    categories = await Category.all()

    response = config.templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "user": user, 
            "item_blocks": {
                category.title: items
            }, 
            "cart_items": cart_items, 
            "categories": categories
        }
    )

    return response
