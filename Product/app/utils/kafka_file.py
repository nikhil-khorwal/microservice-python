import asyncio
from cmath import log
import datetime
from kafka import KafkaConsumer
import json
from kafka import KafkaProducer
import uuid
import json
from time import sleep



def produce_data():
    try:   
        print("start produce")
        producer = KafkaProducer(bootstrap_servers='kafka:9093',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        for _ in range(10):
            the_dt = str(datetime.datetime.utcnow())
            val = f"Count: {_} at {the_dt}"
            print(val)
            producer.send(topic="product_topic", value=val)
    except Exception as e:
        print("err",e)
    else:
        print("end producer")
        producer.close()
