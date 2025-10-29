import enum
from sqlalchemy.dialects.postgresql import ENUM

product_type = ENUM(
    'by weight', 'by portion', name='product_type', create_type=False
)


class ProductsTypes(str, enum.Enum):
    by_weight = 'by weight'
    by_portion = 'by portion'


class DeliveryType(str, enum.Enum):
    delivery = 'delivery'
    contactless_delivery = 'contactless delivery'
    own_collection = 'own collection'
