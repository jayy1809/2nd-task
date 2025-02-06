from fastapi import FastAPI
from app.apis import auth_routes, test_role, product_routes, user_routes, cart_routes, order_routes, complaint_routes
import uvicorn


app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(test_role.router, prefix="/test", tags=["test"])
app.include_router(product_routes.router, prefix="/products", tags=["product"])
app.include_router(user_routes.router, prefix="/users", tags=["user"])
app.include_router(cart_routes.router, tags=["cart"])
app.include_router(order_routes.router, tags=["order"])
app.include_router(complaint_routes.router, tags=["complaint"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the main application!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)