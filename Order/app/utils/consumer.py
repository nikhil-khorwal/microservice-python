from cmath import log
from kafka import KafkaConsumer
import json
from kafka import KafkaProducer
import uuid
import json
from time import sleep

def consume_data():
    consumer = KafkaConsumer('product_kafka',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer = json.loads)
    print("consumer working")
    for msg in consumer:
        print(msg.value)

def produce_data(data):
    producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    for _ in range(10):
        data = {"id": str(uuid.uuid4())}
        print(data)
        producer.send('product_kafka',value=data )
        producer.flush()
        sleep(1)