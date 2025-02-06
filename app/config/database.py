from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings
class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URI)
        self.db = self.client[settings.DB_NAME]
        self.user_collection = self.db["users"]
        self.product_collection = self.db["products"]
        self.cart_collection = self.db["carts"]
        self.order_collection = self.db["orders"]
        self.complaint_collection = self.db["complaints"]

    def get_user_collection(self):
        return self.user_collection
    
    def get_db(self):
        return self.db
database = Database()

async def get_database():
    return database.get_db()
# from motor.motor_asyncio import AsyncIOMotorClient
# from app.config.settings import settings

# client = AsyncIOMotorClient(settings.MONGO_URI, maxPoolSize=10, minPoolSize=1)
# database = client[settings.DB_NAME]
# users_collection = database["users"]


# async def get_database():
#     return database