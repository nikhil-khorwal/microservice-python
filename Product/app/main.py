import asyncio
from re import T
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI,status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
import psycopg2
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from product_kafka.consumer import Consumer
from api.api import products
from psycopg2.extras import LogicalReplicationConnection

load_dotenv()

app = FastAPI()

loop = asyncio.get_event_loop()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request,exc):
    error_dict={}
    for error in exc.errors():
       error_dict[error['loc'][-1]]=error['msg']
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"error": error_dict,"code":400}),
    )


@app.get("/")
def check():
    return {"root":"Product service is working"}
    
def consume(msg):
    print("psycopg2",msg.payload)

@app.on_event("startup")
async def app_startup():
    try:
        my_connection  = psycopg2.connect(
                    "dbname='product' host='db' user='postgres' password='postgres'" ,
                    connection_factory = LogicalReplicationConnection)
        cur = my_connection.cursor()
        cur.create_replication_slot('test_slot', output_plugin = 'wal2json')
        cur.start_replication(slot_name = 'test_slot', options = {'pretty-print' : 1}, decode= True)
        cur.consume_stream(consume)
        loop.run_until_complete(Consumer.consume_data(loop))
    except Exception as e:
        print(e)

app.include_router(products,prefix="/products")


if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)