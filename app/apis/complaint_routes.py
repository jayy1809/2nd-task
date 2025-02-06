from fastapi import APIRouter, Depends, Response, Request, status, Form, UploadFile
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.controllers.complaint_controller import ComplaintController
from app.utils.dependencies import RoleChecker
from app.utils.cloud_upload import upload_to_cloud
from app.models.schemas.complaint_schema import ComplaintCreate
# from app.models.schemas.order_schema import OrderItem, Order

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()
'''

self.user_id = user_id
        self.order_id = order_id
        self.product_id = product_id
        self.issue = issue
        self.image_url = image_url
        self.status = status
'''

@router.post("/complaints/")
async def create_complaint(
    request: Request,
    order_id : str = Form(...),
    product_id : str = Form(...),
    issue : str = Form(...),
    image : UploadFile = Form(None),
    status: str = Form(None),
    complaint_controller : ComplaintController = Depends(ComplaintController),
    payload = Depends(RoleChecker(['admin', 'buyer']))
):
    if image:
        image_url = await upload_to_cloud(image)

    
    user_id = payload.get("sub")

    complaint_detail ={
        "user_id" : user_id,
        "order_id" : order_id,
        "product_id" : product_id,
        "issue" : issue,
        "image_url" : image_url,
        "status" : status
    }

    complaint_dict = ComplaintCreate(**complaint_detail)

    result = await complaint_controller.create_complaint(complaint_dict)
    
    return {
        "data": {"complaint_id" : result},
        "status_code": status.HTTP_201_CREATED,
        "detail": "Complaint created successfully",
        "error": ""
    }