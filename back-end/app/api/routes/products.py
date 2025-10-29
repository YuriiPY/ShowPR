from fastapi import APIRouter, HTTPException, Query, Request, Depends, Header
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from app.db.crud.menu.crud import *
from app.schemas.products import *
from app.db.models.Menu.products_models import *
from app.db.models.Menu.table_names import TableNames
from app.utils.handle_store import get_store_status_data
from app.api.security.admin_auth import admin_auth
# from app.utils.handle_menu_cache import get_menu_cache, set_menu_cache, is_cache_expired, delete_menu_cache #DECIDE WHAT TO DO WITH CACHE DATA

router = APIRouter(
    prefix='/products'
)

tables = {
    'dumplings': Dumplings,
    'soups': Soups,
    'meats': Meats,
    'cakes': Cakes,
}


@router.post('/create/{table}',
             response_model=ItemsResponse,
             dependencies=[Depends(admin_auth)])
async def create_product(
        table: str,
        body: ItemsCreate,
        db: AsyncSession = Depends(get_db)
):
    table_model = tables.get(table)
    if not table_model:
        raise HTTPException(status_code=404, detail='Table not found!')

    try:
        new_item = await create_menu_product(
            table=table_model,
            db=db,
            item=body
        )

        # await delete_menu_cache()

        return ItemsResponse(
            id=new_item.id,
            name=new_item.name,
            name_ua=new_item.name,
            name_pl=new_item.name,
            description=new_item.description,
            description_ua=new_item.description,
            description_pl=new_item.description,
            price=new_item.price,
            type=new_item.type,
            img=new_item.img,
            status=new_item.status
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/get/{table}/{id}', response_model=ItemsResponse)
async def get_product_by_id(
        table: str,
        id: int,
        db: AsyncSession = Depends(get_db)
):
    table_model = tables.get(table)
    if not table_model:
        raise HTTPException(status_code=404, detail='Table not found!')

    try:
        if id:
            item = await get_item_by_id(table_model, id, db)

            return ItemsResponse(
                id=item.id,
                name=item.name,
                name_ua=item.name,
                name_pl=item.name,
                description=item.description,
                description_ua=item.description,
                description_pl=item.description,
                price=item.price,
                type=item.type,
                img=item.img,
                status=item.status
            )
        else:
            items = await get_all_items(table_model, db)

            return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=(str(e)))


@router.get('/get/all')
async def get_products(
        db: AsyncSession = Depends(get_db)
):
    all_data = {}

    try:
        for table in tables.values():
            item = await get_all_items(table, db)
            if item:
                all_data[table.__tablename__] = item

        return all_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=(str(e)))


@router.get('/get-menu')
async def get_menu(
    db: AsyncSession = Depends(get_db)
):
    global _get_menu_cache_data, _get_menu_cache_data

    menu = await get_all_data_from_tables(db)
    result = await get_all_items(TableNames, db)

    cooked_table_names = {}
    frozen_table_names = {}

    # menu_cache = await get_menu_cache()

    # if await is_cache_expired:

    for table_name in result:
        target_dict = frozen_table_names if "frozen_" in table_name.table_name else cooked_table_names

        target_dict[table_name.table_name] = {
            "translation_ua": table_name.translation_ua,
            "translation_en": table_name.translation_en,
            "translation_pl": table_name.translation_pl,
        }

        # menu_data = await set_menu_cache(
        #     data={
        #         "TableNames": {
        #             "cookedTableNames": cooked_table_names,
        #             "frozenTableNames": frozen_table_names
        #         },
        #         "Menu": menu
        #     }
        # )

    return {
        "TableNames": {
            "cookedTableNames": cooked_table_names,
            "frozenTableNames": frozen_table_names
        },
        "Menu": menu
    }

    # return menu_cache


@router.put('/update/{table}/{id}',
            response_model=ItemsResponse, dependencies=[Depends(admin_auth)])
async def update_products(
        table: str,
        id: int,
        body: ItemsUpdate,
        db: AsyncSession = Depends(get_db)
):

    table_model = tables.get(table)
    if not table_model:
        raise HTTPException(status_code=404, detail='Table not found!')

    item = await get_item_by_id(table_model, id, db)
    if not item:
        raise HTTPException(status_code=404, detail='item not found')

    try:
        fields = body.model_dump(exclude_unset=True)
        updated_item = await update_item(table_model, id, db, **fields)

<<<<<<< HEAD
        return ItemsResponse(
            id=updated_item.id,
            name=updated_item.name,
            name_ua=updated_item.name,
            name_pl=updated_item.name,
            description=updated_item.description,
            description_ua=updated_item.description,
            description_pl=updated_item.description,
            price=updated_item.price,
            type=updated_item.type,
            img=updated_item.img,
            status=updated_item.status
        )
=======
        if updated_item:
            # await delete_menu_cache()

            return ItemsResponse(
                id=item.id,
                name=item.name,
                name_ua=item.name,
                name_pl=item.name,
                description=item.description,
                description_ua=item.description,
                description_pl=item.description,
                price=item.price,
                type=item.type,
                img=item.img,
                status=item.status
            )
>>>>>>> 111feba (animation added to front-end)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/delete/{table}/{id}', dependencies=[Depends(admin_auth)])
async def delete_item(
    table: str,
    id: int,
    db: AsyncSession = Depends(get_db)
):
    table_model = tables.get(table)
    if not table_model:
        raise HTTPException(status_code=404, detail='Table not found!')

    item = await get_item_by_id(table_model, id, db)
    if not item:
        raise HTTPException(status_code=404, detail='item not found')

    try:
        # await delete_menu_cache()

        await db.delete(item)
        await db.commit()
        return f'Item with name: {item.name}, was deleted successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
