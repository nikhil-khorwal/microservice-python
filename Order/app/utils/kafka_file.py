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
        producer = KafkaProducer(bootstrap_servers=['kafka:9092'])
        for _ in range(10):
            the_dt = str(datetime.datetime.utcnow())
            val = f"Count: {_} at {the_dt}".encode(encoding='utf8')
            print(val)
            producer.send(topic="mytopic", value=val)
        # producer.send("mytopic", value="Count: at ".encode(encoding='utf8'))
        # producer.flush()
    except Exception as e:
        print("err",e)
    else:
        print("end producer")
        producer.close()

def consume_data():
    consumer = KafkaConsumer( 
        bootstrap_servers=['host.docker.internal:9092'],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="group_id",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    consumer.subscribe(['mytopic'])

    for message in consumer:
        try:
            kafka_message = f"""
            Message received: {message.value}
            Message key: {message.key}
            Message partition: {message.partition}
            Message offset: {message.offset}
            """
            print(kafka_message)
        except Exception as e:
            print(e)
    