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

from datetime import datetime
from pydantic import BaseModel

class OrderEnum(enum.Enum):
    CANCELLED = "cancelled"
    SUCCESS = "success"
    PENDING = "pending"


class OrderTable(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100))
    phone = Column(String(13))
    created_at = Column(String(100), default=datetime.now())
    updated_at = Column(String(100), default=datetime.now())
    status = Column(String(13))
    product_id = Column(Integer)
    is_delete = Column(Boolean, default=False)


class order_model(BaseModel):
    email :str
    phone:str
    status:str
    product_id:int