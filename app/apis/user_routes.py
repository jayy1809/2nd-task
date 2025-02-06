from fastapi import APIRouter, Depends, Response, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.controllers.user_controller import UserController
from app.utils.dependencies import RoleChecker
from app.models.schemas.user_schema import UserUpdate

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.get("/") # prefix will be /users in main.py
@limiter.limit("5/minute")
async def get_users(
    request: Request,
    user_controller : UserController = Depends(UserController),
    payload = Depends(RoleChecker(['admin']))
):
    result = await user_controller.get_users()
    return {
        "data": result,
        "status_code": status.HTTP_200_OK,
        "detail": "Get users successful",
        "error": ""
    }

@router.get("/me")
@limiter.limit("5/minute")
async def get_user_by_id(
    request: Request,
    user_controller : UserController = Depends(UserController),
    payload = Depends(RoleChecker(['admin', 'user', 'seller']))
):
    result = await user_controller.get_user_by_id(payload.get("sub"))
    return {
        "data": result,
        "status_code": status.HTTP_200_OK,
        "detail": "Get user successful",
        "error": ""
    }

@router.put("/{user_id}/role")
@limiter.limit("5/minute")
async def update_user_role(
    user_id: str,
    request: Request,
    update_user: UserUpdate,
    user_controller : UserController = Depends(UserController),
    payload = Depends(RoleChecker(['admin']))
):
    result = await user_controller.update_user_role(user_id, update_user)
    return {
        "data": result,
        "status_code": status.HTTP_200_OK,
        "detail": "User Role updated successfully",
        "error": ""
    }