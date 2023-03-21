from kafka import KafkaProducer
import uuid
import json
from time import sleep

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for _ in range(10):
    data = {"id": str(uuid.uuid4())}
    print(data)
    producer.send('product_kafka',value=data )
    producer.flush()
    sleep(1)