import asyncio
import datetime
import json
import os
from fastapi import APIRouter, BackgroundTasks,Depends,status
from kafka import KafkaProducer
from order_kafka.producer import Producer
from api.base import get_db
from api.model import OrderTable,order_model
from fastapi.responses import JSONResponse
import requests
from fastapi import HTTPException

orders = APIRouter()

@orders.get("/")
async def get_all_orders(background_task:BackgroundTasks,Session = Depends(get_db)):
    session = Session()
    res = session.query(OrderTable).all()
    return res
    
@orders.post("/")
async def create_order(data:order_model, session = Depends(get_db)):
    response = requests.get(f"{os.environ.get('PRODUCT_SERVICE_URL')}/products/{data.product_id}")
    if(response.status_code==404):
        return JSONResponse(status_code= status.HTTP_404_NOT_FOUND,content={"message":"product not found"})
    product = json.loads(response.content)
    if(data.quantity > product.get('stock')):
        return JSONResponse(status_code= status.HTTP_400_BAD_REQUEST,content={"message":"quantity is greater then stock"})
    new_order = OrderTable(
        email = data.email,
        phone = data.phone,
        quantity = data.quantity,
        product_id = data.product_id)
        
    await Producer.create_order(order_model.from_orm(new_order).dict())
    
    session.add(new_order)
    session.commit()
    
    return JSONResponse(content={"message":"order created sucessfully"}, status_code=status.HTTP_201_CREATED)


@orders.get("/{order_id}")
async def get_all_products(order_id:int, Session = Depends(get_db)):
    session = Session()
    res = session.query(OrderTable).filter(OrderTable.id == order_id).first()
    
    if(res is None):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message":"order not found"})
    
    return res