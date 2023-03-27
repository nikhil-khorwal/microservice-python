import json
from aiokafka import AIOKafkaConsumer
# import pypgoutput

class Consumer:
    @staticmethod
    def create_consumer(loop):
        return AIOKafkaConsumer('order_topic',loop=loop,
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

    async def check_events(event):
        print(event)


# def cdc_reader():
#     cdc_reader = pypgoutput.LogicalReplicationReader(
#                 publication_name="test_pub",
#                 slot_name="test_slot",
#                 host="db",
#                 database="product",
#                 port=5432,
#                 user="postgres",
#                 password="postgres",)
#     for message in cdc_reader:
#         print(message.json(indent=2))


#   cdc_reader()