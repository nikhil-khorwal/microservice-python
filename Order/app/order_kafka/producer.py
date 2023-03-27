import asyncio
import json
from aiokafka import AIOKafkaProducer
from kafka import KafkaProducer


class Producer:
  @staticmethod
  def create_producer():
    return AIOKafkaProducer(bootstrap_servers=['kafka:9093'],
        key_serializer=lambda v: json.dumps(v).encode('utf-8'),
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))

  @staticmethod
  async def create_order(data):
    try:
        producer:AIOKafkaProducer = Producer.create_producer()
        await producer.start()
        await producer.send_and_wait(topic="product_topic",key="create_order",value=data)
    except Exception as error:
        print("Order producer error : ",error)
    finally:
      await producer.stop()