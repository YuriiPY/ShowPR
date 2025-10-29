from typing import Union
from pydantic import BaseModel

from app.db.enums import ProductsTypes


class ItemsCreate(BaseModel):
    name: str
    name_ua: str
    name_pl: str
    price: int
    type: ProductsTypes
    status: bool
    img: Union[str, None] = "https://i.ibb.co/Q33Zbq12/unfinded.webp"
    description: Union[str, None] = None
    description_ua: Union[str, None] = None
    description_pl: Union[str, None] = None


class ItemsUpdate(BaseModel):
    name: Union[str, None] = None
    name_ua: Union[str, None] = None
    name_pl: Union[str, None] = None
    description: Union[str, None] = None
    description_ua: Union[str, None] = None
    description_pl: Union[str, None] = None
    price: Union[int, None] = None
    type: ProductsTypes
    img: Union[str, None] = None
    status: Union[bool, None] = None


class ItemsResponse(BaseModel):
    id: int
    name: str
    name_ua: str
    name_pl: str
    description: Union[str, None] = None
    description_ua: Union[str, None] = None
    description_pl: Union[str, None] = None
    price: int
    type: ProductsTypes
    img: Union[str, None] = None
    status: bool

    class Config:
        orm_mode = True
