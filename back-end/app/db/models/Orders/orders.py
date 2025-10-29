from sqlalchemy import Column, Integer, VARCHAR, TEXT, DATE, TIME
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from app.db.base import Base


class Orders(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": "order_data"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False)
    phone_number = Column(VARCHAR(20), nullable=False)
    email = Column(VARCHAR(255))
    items = Column(JSONB, nullable=False)
    total_amount = Column(Integer, nullable=False)
    delivery_time = Column(TEXT, nullable=False, default='asap')
    delivery_method = Column(ENUM(
        'delivery',
        'contactless delivery',
        'own collection',
        name='delivery_type',
        schema='order_data'
    ), nullable=False)
    location = Column(JSONB)
    status = Column(ENUM(
        'pending',
        'ready to delivery',
        'processing',
        'shipped',
        'delivered',
        'canceled',
        'returned',
        name='order_status',
        schema='order_data'
    ),
        nullable=False,
        default="pending"
    )
    delivery_time = Column(TIME)
    delivery_date = Column(DATE, nullable=False)
