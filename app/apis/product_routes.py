from fastapi import APIRouter, Depends, Response, Request, status, Form, UploadFile, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.controllers.product_controller import ProductController
from app.utils.dependencies import RoleChecker
from app.models.schemas.product_schema import ProductUpdate, ProductCreate
from app.utils.cloud_upload import upload_to_cloud

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.get("/preload-data", response_model=None)
@limiter.limit("5/minute")
async def preload_data(
    request: Request,
    preload_controller : ProductController = Depends(ProductController),
):
    result = await preload_controller.preload_data()
    return {
        "data": result,
        "status_code": status.HTTP_201_CREATED,
        "detail": "Preload data successful",
        "error": ""
    }

@router.get("/") # prefixed with /products in main.py
@limiter.limit("5/minute")
async def get_products(
    request: Request,
    preload_controller : ProductController = Depends(ProductController),
):
    result = await preload_controller.get_products()
    return {
        "data": result,
        "status_code": status.HTTP_200_OK,
        "detail": "Get products successful",
        "error": ""
    }


@router.post("/")
@limiter.limit("5/minute")
async def create_product(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    price: float = Form(...),
    rating: float = Form(...),
    brand: str = Form(...),
    image: UploadFile = Form(...),
    thumbnail: str = Form(None),
    payload: dict = Depends(RoleChecker(["seller"])),
    product_controller : ProductController = Depends(ProductController),
):
    seller_id = payload.get("sub")

    try : 
        thumbnail_url = None
        if thumbnail is not None:
            thumbnail_url = await upload_to_cloud(thumbnail)

        file_url = await upload_to_cloud(image)
        product_data = {
            "title": title,
            "description": description,
            "category": category,
            "price": price,
            "rating": rating,
            "brand": brand,
            "images": [file_url],
            "seller_id": seller_id,
            "thumbnail": thumbnail_url
        }

        product_dict = ProductCreate(**product_data)
        result = await product_controller.create_product(product_dict)
        return {
            "data": result,
            "status_code": status.HTTP_201_CREATED,
            "detail": "Create product successful",
            "error": ""
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{product_id}")
@limiter.limit("5/minute")
async def download_product(
    product_id: str,
    request: Request,
    preload_controller : ProductController = Depends(ProductController),
):
    result = await preload_controller.download_product(product_id)
    return result


@router.get("/{product_id}")
@limiter.limit("5/minute")
async def get_product_by_id(
    product_id: str,
    request: Request,
    preload_controller : ProductController = Depends(ProductController),
):
    result = await preload_controller.get_product_by_id(product_id)
    return {
        "data": result,
        "status_code": status.HTTP_200_OK,
        "detail": "Get product by id successful",
        "error": ""
    }









@router.put("/{product_id}")
@limiter.limit("5/minute")
async def update_product(
    product_id: str,
    request: Request,
    product_update_data: ProductUpdate,
    token_data: dict = Depends(RoleChecker(["seller"])),
    product_controller : ProductController = Depends(ProductController),
):
    seller_id = token_data.get("sub")
    updated_product = await product_controller.update_product(product_id, seller_id, product_update_data.model_dump(exclude_unset=True))
    return {
        "data": updated_product,
        "status_code": status.HTTP_200_OK,
        "detail": "Update product successful",
        "error": ""
    }

@router.delete("/{product_id}")
@limiter.limit("5/minute")
async def delete_product(
    product_id: str,
    request: Request,
    token_data: dict = Depends(RoleChecker(["seller"])),
    product_controller : ProductController = Depends(ProductController),
):
    seller_id = token_data.get("sub")
    result = await product_controller.delete_product(product_id, seller_id)
    return {
        "data_deleted": result,
        "status_code": status.HTTP_200_OK,
        "detail": "Delete product successful",
        "error": ""
    }


    # return {
    #     "data": result,
    #     "status_code": status.HTTP_200_OK,
    #     "detail": "Download product successful",
    #     "error": ""
    # }

