from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["orders"])


@order_router.post("/")
def order():
    return {"message: order message for customers"}
