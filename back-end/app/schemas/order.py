from typing import Dict, Optional, Union
from pydantic import BaseModel, RootModel

from app.db.enums import DeliveryType


class Additions(BaseModel):
    cutlery: int
    onion: int
    cream: int


class ProductData(BaseModel):
    tableName: str
    productId: int
    quantity: int | None
    weight: int | None
    additions: Additions


class BasketAmount(RootModel[Dict[str, ProductData]]):
    pass


class userLocationData(BaseModel):
    street: str
    home: str
    homeNumber: str


class OrderData(BaseModel):
    name: str
    phone_number: str
    email: str
    total_amount: int
    items: Dict[str, ProductData]
    delivery_time: str
    delivery_method: DeliveryType
    location: userLocationData


class LocationData(BaseModel):
    lat: float
    long: float
