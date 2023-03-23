import asyncio
import json
from aiokafka import AIOKafkaProducer
from fastapi import BackgroundTasks, FastAPI,status
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from utils.kafka_file import produce_data
from utils.kafka_file import consume_data
from api.api import  orders
from kafka.admin import NewTopic, ConfigResource, ConfigResourceType
from kafka.errors import TopicAlreadyExistsError
load_dotenv()



app = FastAPI()

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
    return {"root":"Order service is working"}

app.include_router(orders,prefix="/orders")

async def send_one():
    producer = AIOKafkaProducer(
            loop=asyncio.get_event_loop(), bootstrap_servers=["kafka:9092"],
            max_batch_size=10000)
    await producer.start()
    # producer = AIOKafkaProducer(loop=asyncio.get_event_loop(),
    #     bootstrap_servers=':9092')
    # await producer.start()
    # while True:
    #     try:
    #         res = await producer.send_and_wait("mytopic", b"Super message")
    #         print(res)
    #         await asyncio.sleep(1)
    #     except:
    #         await producer.stop()
    #         raise



@app.on_event('startup')
def start():
    print("start")
    asyncio.create_task(send_one())
    

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8001,reload=True,workers=3)


