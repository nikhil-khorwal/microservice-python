from kafka import KafkaConsumer
import json

class OrderConsumer:
    def __init__(self) -> None:
        self.consumer = KafkaConsumer('order_kafka',
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            value_deserializer = json.loads)

    def read(self):
        for msg in self.consumer:
            print(msg.value)