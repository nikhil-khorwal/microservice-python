from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
import os
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2.extras import LogicalReplicationConnection
Base = declarative_base()

def get_db():
    connection_string = os.environ.get("PRODUCT_DB_URI")
    engine = create_engine(connection_string)

    def recreate_database():
        Base.metadata.create_all(engine)

    recreate_database()
    Session = sessionmaker(bind=engine)
    return Session

