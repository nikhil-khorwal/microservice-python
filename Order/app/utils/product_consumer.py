import datetime
import json

from kafka import KafkaConsumer, KafkaProducer


def produce_data():
    try:   
        print("start produce")
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
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

produce_data()

