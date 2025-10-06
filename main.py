from fastapi import FastAPI
from auth_routes import auth_router as myauth
from order_routes import order_router as myorder

app = FastAPI(title="Food Delivery App")

app.include_router(myauth)
app.include_router(myorder)
