from fastapi import APIRouter, Depends, Response, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.controllers.order_controller import OrderController
from app.utils.dependencies import RoleChecker
from app.models.schemas.order_schema import OrderItem, Order

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.post("/orders/")
@limiter.limit("5/minute")
async def create_order(
    # order_data: Order,
    request: Request,
    order_controller : OrderController = Depends(OrderController),
    payload = Depends(RoleChecker(['admin', 'buyer']))
):
    user_id = payload.get("sub")
    result = await order_controller.create_order(user_id)
    
    return {
        "data": {"order_id" : result},
        "status_code": status.HTTP_201_CREATED,
        "detail": "Order created successfully",
        "error": ""
    }

@router.get("/orders/")
@limiter.limit("5/minute")
async def get_order_history(
    request: Request,
    order_controller : OrderController = Depends(OrderController),
    payload = Depends(RoleChecker(['admin', 'buyer']))
):
    user_id = payload.get("sub")
    result = await order_controller.get_order_history(user_id)
    
    return {
        "data": result,
        "status_code": status.HTTP_200_OK,
        "detail": "Order history retrieved successfully",
        "error": ""
    }

@router.get("/orders/{order_id}")
@limiter.limit("5/minute")
async def get_order_by_id(
    order_id: str,
    request: Request,
    order_controller : OrderController = Depends(OrderController),
    payload = Depends(RoleChecker(['admin', 'buyer']))
):
    user_id = payload.get("sub")
    result = await order_controller.get_order_by_id(user_id, order_id)
    
    return {
        "data": result,
        "status_code": status.HTTP_200_OK,
        "detail": "Order of particular id retrieved successfully",
        "error": ""
    }