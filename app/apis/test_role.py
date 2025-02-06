from fastapi import APIRouter, Depends
from app.utils.dependencies import RoleChecker

router = APIRouter()

@router.get("/protected-admin-route")
async def protected_admin_route(
    payload: dict = Depends(RoleChecker(["admin"]))
):
    return {
        "data": {"message": "This is protected admin data", "user_id": payload.get("sub")},
        "status_code": 200,
        "detail": "Success",
        "error": ""
    }