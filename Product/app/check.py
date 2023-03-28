import asyncio
import psycopg2
from psycopg2.extras import ReplicationCursor,LogicalReplicationConnection
connection = {
    'host': '127.0.0.1',
    'port': 5432,
    'database': 'product',
    'user': 'postgres',
    'password': 'postgres',
}
my_connection  = psycopg2.connect(**connection, connection_factory = LogicalReplicationConnection)
cur:ReplicationCursor = my_connection.cursor()
# self.cur.execute("CREATE PUBLICATION product_pub FOR ALL TABLES;")
cur.drop_replication_slot('test_slot')
cur.create_replication_slot('test_slot', output_plugin = 'pgoutput')
cur.start_replication(slot_name = 'test_slot',  decode= True, options={"proto_version": 1,"publication_names": ["product_pub"]})

async def get():
  while True:
    try:
        await asyncio.sleep(1)
        message = cur.read_message()
        if message is not None:
            print("message",message)
    except Exception as e:
        print("Error,",e)

get()