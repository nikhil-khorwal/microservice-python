import asyncio
from base64 import encode
import json
from re import T
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI,status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
import psycopg2
from sqlalchemy import null
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from product_kafka.consumer import Consumer
from api.api import products
from psycopg2.extras import LogicalReplicationConnection,ReplicationCursor,ReplicationMessage
import codecs
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
    print("start replication")
    print("psycopg2",msg.payload)


class BackgroundRunner:
    def __init__(self):
        connection = {
            'host': 'db',
            'port': 5432,
            'database': 'product',
            'user': 'postgres',
            'password': 'postgres',
        }
        my_connection  = psycopg2.connect(**connection,
                    connection_factory = LogicalReplicationConnection)
        self.cur:ReplicationCursor = my_connection.cursor()
        # self.cur.execute("CREATE PUBLICATION product_pub FOR ALL TABLES;")
        self.cur.drop_replication_slot('test_slot')
        self.cur.create_replication_slot('test_slot', output_plugin = 'pgoutput')
        self.cur.start_replication(slot_name = 'test_slot',   options={"proto_version": 1,"publication_names": "product_pub"})
        # self.cur.execute("SELECT * FROM pg_logical_slot_get_changes('test_slot', NULL, NULL)")
    async def run_main(self):
        # for change in self.cur:
        #     print(change)
        while True:
            await asyncio.sleep(1)
            message = self.cur.read_message()
            
            
            if message is not None:
                print(codecs.decode(message.payload))
                
                # print(message.payload.decode('utf-8'))
            # if message is not None:
            #     data = message.payload.decode('utf-8')
            #     print(type(data))
            # if message is not None:
            #     print("message",message)




@app.on_event("startup")
async def app_startup():
    runner = BackgroundRunner()
    asyncio.create_task(runner.run_main())
      

app.include_router(products,prefix="/products")


if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)