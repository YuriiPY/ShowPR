import aiohttp
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from geopy.geocoders import Nominatim
from geopy.adapters import AioHTTPAdapter

from app.db.crud.menu.crud import _get_table_models_in_schema, _get_tables_in_schema
from app.db.session import get_db
from app.schemas.order import BasketAmount, LocationData, OrderData
from app.schemas.products import ItemsResponse
from app.db.crud.menu.crud import *
from app.db.models.Orders.orders import Orders
from app.core.config import TG_BOT_URL

router = APIRouter(
    prefix='/order'
)

tables = {
    'dumplings': Dumplings,
    'soups': Soups,
    'meats': Meats,
    'cakes': Cakes,
    'frozen_dumplings': Frozen_Dumplings,
    'frozen_meats': Frozen_Meats,
}

# TEST ROUT FOR GETTING TABLE MODELS
# @router.get('/get_tables')
# async def basket_amount(
#     db: AsyncSession = Depends(get_db)
# ):

#     tables = await _get_tables_in_schema(db, "menu")
#     tables_info = []
#     for table_name, table in tables.items():
#         tables_info.append({
#             "table_name": table_name,
#             "columns": [col.name for col in table.columns]
#         })

#     table_key = f"menu.dumplings"

#     table_model = tables.get(table_key)

#     print("Test table here ->", table_model)

#     for col in table_model.columns:
#         print(f"-{col.name} ({col.type})\n")

#     return tables_info


@router.post('/get_amount')
async def basket_amount(
    basket: BasketAmount,
    db: AsyncSession = Depends(get_db)
):
    total_amount = 0
    response = {
        "products": {},
        "totalAmount": 0
    }
    print("items", basket.root.items(), "end")

    for product_name, product_data in basket.root.items():

        table_model = tables.get(product_data.tableName)

        if not table_model:
            raise HTTPException(status_code=404, detail='Table not found!')

        item: ItemsResponse = await get_item_by_id(table_model, product_data.productId, db)

        if not item:
            raise HTTPException(status_code=404, detail='Item not found!')

        if item.status:
            product_amount = (item.price * product_data.quantity) + (
                2 * product_data.additions.cream) + (2 * product_data.additions.onion) + (2 * product_data.additions.cutlery)

            total_amount += product_amount
            response["products"][product_name] = product_amount

        else:
            response["products"][product_name] = None

    response["totalAmount"] = total_amount
    return response


# @router.post('/send_code')
# async def verify_phone(
#     phone: str
# ):
#     random_number = random.randint(100000, 999999)
#     return random_number


@router.post('/get_location')
async def get_location(
    data: LocationData
):
    async with Nominatim(
        user_agent="Pierogowa",
        adapter_factory=AioHTTPAdapter
    ) as geo_locator:

        try:
            location = await geo_locator.reverse((data.lat, data.long))
            location = location.raw["address"]

            if "house_number" in location:
                location_response = {
                    "street": location["road"], "home": location["house_number"]}
                return location_response
            else:
                return {"street": location["road"]}
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=500, detail=str(e))


# TODO: SEARCH HOW TO CREATE ROUTE FUNCTION WITH TRY/EXCEPT
@router.post('/add_order')
async def add_order(
    order_data: OrderData,
    db: AsyncSession = Depends(get_db)
):
    verify_total_amount = 0
    product_list = []
    product_name_list = []

    for product_name, product_data in order_data.items.items():
        print("PRODUCT INFORMATION->", product_name, product_data)
        table_model = tables.get(product_data.tableName)
        if not table_model:
            raise HTTPException(status_code=404, detail='Table not found!')

        item: ItemsResponse = await get_item_by_id(table_model, product_data.productId, db)

        if (not item):
            raise HTTPException(status_code=404, detail='Item not found!')

        if item.status:
            verify_total_amount += (
                product_data.quantity * item.price
                + product_data.additions.cream * 2
                + product_data.additions.onion * 2
                + product_data.additions.cutlery * 2
            )
            item_dict = {col.name: getattr(item, col.name)
                         for col in table_model.__table__.columns}
            item_dict["table_name"] = product_data.tableName
            item_dict["additions"] = product_data.additions.model_dump()
            if item.type == "by portion":
                item_dict["quantity"] = product_data.quantity
            elif item.type == "by weight":
                item_dict["weight"] = product_data.weight
            product_list.append(item_dict)
            product_name_list.append(item.name)
        else:
            raise HTTPException(
                status_code=404, detail=f'Product {item.name} is not available now!')

    if verify_total_amount == order_data.total_amount:
        pass

    time_value = None
    if order_data.delivery_time == 'asap':
        pass
    else:
        time_value = datetime.strptime(
            order_data.delivery_time, "%H:%M").time()

    current_date = datetime.now().date()

    new_order = await create_new_item(
        table=Orders,
        db=db,
        field={
            "name": order_data.name,
            "phone_number": order_data.phone_number,
            "email": order_data.email,
            "items": product_list,
            "total_amount": verify_total_amount,
            "delivery_date": current_date,
            "delivery_time": time_value,
            "delivery_method": order_data.delivery_method,
            "location": order_data.location.model_dump()
        }
    )

    try:
        async with aiohttp.ClientSession() as session:
            print(TG_BOT_URL+'/new_msg')
            async with session.post(url=TG_BOT_URL+'/new_msg', json={
                'order_list': product_name_list,
                'order_id': new_order.id
            }) as response:
                result = await response.json()
                print(result)
            print(response)
    except Exception as e:
        print(str(e))

    return new_order
