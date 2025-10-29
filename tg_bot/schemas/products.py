from typing import Optional
from pydantic import BaseModel

from db.enums import ProductsTypes


class ItemsCreate(BaseModel):
    name: str
    price: int
    type: ProductsTypes
    available: bool
    img: Optional[bytes] = None
    description: Optional[str] = None


class ItemsUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    type: Optional[ProductsTypes] = None
    img: Optional[bytes] = None
    available: Optional[bool] = None


class ItemsResponse(BaseModel):
    name: str
    description: Optional[str]
    price: int
    type: ProductsTypes
    img: Optional[bytes]
    available: bool

    class Config:
        orm_mode = True


class OrderRequest(BaseModel):
    order_list: list[str]
    order_id: int
