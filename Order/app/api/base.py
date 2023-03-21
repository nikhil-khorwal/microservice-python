from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
import os
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def get_db():
    connection_string = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            os.environ.get("DB_USER"),
            os.environ.get("DB_PASS"),
            os.environ.get("DB_HOST"),
            os.environ.get("DB_PORT"),
            os.environ.get("DB_NAME"))
    engine = create_engine(connection_string)

    def recreate_database():
        Base.metadata.create_all(engine)

    recreate_database()
    Session = sessionmaker(bind=engine)
    return Session
