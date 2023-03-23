import asyncio
import json
from fastapi import APIRouter, BackgroundTasks,Depends,status
from kafka import KafkaProducer
from utils.kafka_file import consume_data
from utils.kafka_file import produce_data
from api.base import get_db
from api.model import OrderTable,order_model
from fastapi.responses import JSONResponse
import requests
from fastapi import HTTPException
from aiokafka import AIOKafkaProducer

orders = APIRouter()

@orders.get("/")
async def get_all_orders(background_task:BackgroundTasks,Session = Depends(get_db)):
    produce_data()
    session = Session()
    res = session.query(OrderTable).all()
    return res
    
@orders.post("/")
async def create_order(data:order_model, Session = Depends(get_db)):
    session = Session()
    
    product = requests.get("http://host.docker.internal:8000/products/{}".format(data.product_id))
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


@orders.get("/{order_id}")
async def get_all_products(order_id:int, Session = Depends(get_db)):
    session = Session()
    res = session.query(OrderTable).filter(OrderTable.id == order_id).first()
    
    if(res is None):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message":"order not found"})
    
    return res