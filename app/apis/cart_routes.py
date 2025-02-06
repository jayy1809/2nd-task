from fastapi import APIRouter, Depends, Response, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.controllers.user_controller import UserController
from app.utils.dependencies import RoleChecker
from app.models.schemas.cart_schema import CartItem
from app.controllers.cart_controller import CartController

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


@router.post("/cart/add")
@limiter.limit("5/minute")
async def add_to_cart(
    cart_item: CartItem,
    request: Request,
    cart_controller : CartController = Depends(CartController),
    payload = Depends(RoleChecker(['admin', 'buyer']))
):
    user_id = payload.get("sub")
    result = await cart_controller.add_to_cart(user_id, cart_item)
    
    return {
        "data": {"cart_id" : result},
        "status_code": status.HTTP_201_CREATED,
        "detail": "Item added to cart successfully",
        "error": ""
    }

@router.delete("/cart/remove/{product_id}")
@limiter.limit("5/minute")
async def remove_from_cart(
    product_id: str,
    request: Request,
    cart_controller : CartController = Depends(CartController),
    payload = Depends(RoleChecker(['admin', 'buyer']))
):
    user_id = payload.get("sub")
    result = await cart_controller.remove_from_cart(user_id, product_id)
    
    return {
        "data": {
            "result" : f"{result} such Item with product id {product_id} removed from cart successfully"
        },
        "status_code": status.HTTP_200_OK,
        "detail": "Item removed from cart successfully",
        "error": ""
    }

@router.get("/cart/")
@limiter.limit("5/minute")
async def get_cart(
    request: Request,
    cart_controller : CartController = Depends(CartController),
    payload = Depends(RoleChecker(['admin', 'buyer']))
):
    user_id = payload.get("sub")
    result = await cart_controller.get_cart(user_id)
    
    return {
        "data": result,
        "status_code": status.HTTP_200_OK,
        "detail": "Cart items retrieved successfully",
        "error": ""
    }

