from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('product_kafka',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer = json.loads)

for msg in consumer:
    print(msg.value)