import json
from aiokafka import AIOKafkaConsumer
from product_kafka.events import Events


class Consumer:
    @staticmethod
    def create_consumer(loop):
        return AIOKafkaConsumer('product_topic',loop=loop,
            bootstrap_servers="kafka:9093",   
            auto_offset_reset='latest',
            key_deserializer=lambda v: json.loads(v),
            value_deserializer=lambda v: json.loads(v))

    @staticmethod
    async def consume_data(loop):
        consumer = Consumer.create_consumer(loop)
        await consumer.start()
        try:
            async for msg in consumer:
                await Consumer.check_events(msg)
        finally:
            print("stop")
            await consumer.stop()
            print(consumer._closed)

    async def check_events(event):
        events = Events()
        print(event)
        if event.key == 'create_order':
            await events.create_order(event)
