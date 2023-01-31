from fastapi import APIRouter,Depends,status
from api.base import get_db
from api.model import OrderTable,order_model
from fastapi.responses import JSONResponse
import requests
from fastapi import HTTPException

orders = APIRouter()

@orders.get("/")
async def get_all_orders(Session = Depends(get_db)):
    session = Session()
    res = session.query(OrderTable).all()
    return res

@orders.post("/")
async def create_order(data:order_model, Session = Depends(get_db)):
    print("data",data)
    session = Session()
    
    product = requests.get("http://192.168.0.107:8000/products/{}".format(data.product_id))
    if(product.status_code==404):
        return JSONResponse(status_code= status.HTTP_404_NOT_FOUND,content={"message":"product not found"})
    
    new_order = OrderTable(
    email = data.email,
    phone = data.phone,
    status = data.status,
    product_id = data.product_id)

    session.add(new_order)
    session.commit()

    return JSONResponse(content={"message":"order created sucessfully"}, status_code=status.HTTP_201_CREATED)