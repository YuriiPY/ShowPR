from enum import Enum
from sqlalchemy import Boolean, Column, Integer, LargeBinary, String
from sqlalchemy.dialects.postgresql import ENUM

from app.db.base import Base
from app.db.enums import product_type, ProductsTypes


class ProductModel(Base):
    __abstract__ = True
    __table_args__ = {'schema': 'menu'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    name_ua = Column(String, nullable=False)
    name_pl = Column(String, nullable=False)
    description = Column(String(255), default="NONE")
    description_ua = Column(String(255), default="NONE")
    description_pl = Column(String(255), default="NONE")
    price = Column(Integer, nullable=False)
    type = Column(ENUM("by weight", "by portion",
                  name="product_type", schema="menu"), nullable=False)
    img = Column(String, default="https://i.ibb.co/Q33Zbq12/unfinded.webp")
    status = Column(Boolean, nullable=False, default=False)


class Dumplings(ProductModel):
    __tablename__ = 'dumplings'


class Soups(ProductModel):
    __tablename__ = 'soups'


class Meats(ProductModel):
    __tablename__ = 'meats'


class Cakes(ProductModel):
    __tablename__ = 'cakes'


class Frozen_Dumplings(ProductModel):
    __tablename__ = 'frozen_dumplings'


class Frozen_Meats(ProductModel):
    __tablename__ = 'frozen_meats'
