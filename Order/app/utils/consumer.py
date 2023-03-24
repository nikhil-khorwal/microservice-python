import json

from kafka import KafkaConsumer

def consume_data():
    try:   
        print("start consumer")
        consumer = KafkaConsumer('order_topic',
            bootstrap_servers='kafka:9093',
            auto_offset_reset='earliest')
        print(consumer.bootstrap_connected())
        for msg in consumer:
            print(msg.value)
    except Exception as e:
        print("Consumer Error",e)
    else:
        print("end consumer")
        consumer.close()

if __name__ == "__main__":
  consume_data()