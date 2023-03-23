from fastapi import APIRouter, Depends, responses

from application.models import User, MarketItem


router = APIRouter(prefix="/api/cart", tags=["api", "cart"])


@router.put("/add")
async def add_item_to_cart(
    item_id: int, 
    user: User = Depends(User.dependency)
):
    if not user:
        return responses.JSONResponse({"error": "Unauthorized"}, 401)
    
    if not MarketItem.exists(id=item_id):
        return responses.JSONResponse({"error": "Item does not exists"}, 404)
    
    if item_id in user.cart:
        return responses.JSONResponse({"error": "Item is already in the cart"}, 409)
    
    user.cart.append(item_id)
    await user.save()

    return responses.JSONResponse({
        "message": "success"
    }, 200)


@router.delete("/remove")
async def remove_item_from_cart(
    item_id: int, 
    user: User = Depends(User.dependency)
):
    if not user:
        return responses.JSONResponse({"error": "Unauthorized"}, 401)
    
    if item_id not in user.cart:
        return responses.JSONResponse({"error": "Item is not in the cart"}, 409)
    
    user.cart.remove(item_id)
    await user.save()

    return responses.JSONResponse({
        "message": "success"
    }, 200)
