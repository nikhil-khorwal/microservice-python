import enum
from api.base import Base,get_db
from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
    column,
    create_engine,
    Boolean,
    null,
    Float,
)
from pydantic import BaseModel
from datetime import datetime

class ProductTable(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    desc = Column(String(250))
    price = Column(Integer)
    discount_percentage = Column(Float)
    gst_percentage = Column(Float)
    stock = Column(Integer)
    created_at = Column(String(100), default=datetime.now())
    updated_at = Column(String(100), default=datetime.now())
    is_delete = Column(Boolean, default=False)




class product_model(BaseModel):
    title:str
    desc:str
    price:float
    discount_percentage:float
    gst_percentage:float
    stock:float