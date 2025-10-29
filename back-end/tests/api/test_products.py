import pytest
import asyncio
import pytest_asyncio
from httpx import AsyncClient

from app.db.seeds import (
    first_product,
    second_product,
    tables,
    update_data
)
from app.db.enums import ProductsTypes
from app.core.config import ADMIN_NAME, ADMIN_PASSWORD

auth = (
    ADMIN_NAME, ADMIN_PASSWORD
)


@pytest.mark.asyncio
async def test_create_table(client: AsyncClient):
    first_response = await client.post(
        url='/products/create/dumplings',
        json=first_product,
        auth=auth
    )

    assert first_response.status_code == 200
    data = first_response.json()
    assert data['name'] == first_product['name']
    assert data['price'] == first_product['price']

    second_response = await client.post(
        url='/products/create/dumplings',
        json=second_product,
        auth=auth
    )

    assert second_response.status_code == 200
    second_data = second_response.json()
    assert second_data['name'] == second_product['name']
    assert second_data['price'] == second_product['price']


@pytest.mark.asyncio
async def test_get_product(client: AsyncClient):
    response = await client.get(f'/products/get/{tables[0]}/1')

    assert response.status_code == 200, f"Details: {response.json()}"
    product_data = response.json()
    assert type(product_data['name']) == str
    assert type(product_data['price']) == int

# issubclass What is it? and check hasattr


@pytest.mark.asyncio
async def test_get_all_products(client: AsyncClient):
    response = await client.get('/products/get/all')

    assert response.status_code == 200, f"Details: {response.json()}"
    data = response.json()

    assert isinstance(data, dict)
    assert len(data) > 0

    for table, list_items in data.items():
        assert isinstance(table, str)
        assert isinstance(list_items, list)

        for item in list_items:
            assert isinstance(item, dict)

            assert isinstance(item["id"], int)
            assert isinstance(item["name"], str)
            assert isinstance(item["name_ua"], str)
            assert isinstance(item["name_pl"], str)
            assert isinstance(item["description"], str)
            assert isinstance(item["description_ua"], str)
            assert isinstance(item["description_pl"], str)
            assert item["type"] in ProductsTypes._value2member_map_
            assert isinstance(item["status"], bool)
            assert isinstance(item["price"], (int, float))
            assert isinstance(item["img"], str)


@pytest.mark.asyncio
async def test_get_menu(client: AsyncClient):
    response = await client.get('/products/get-menu')

    assert response.status_code == 200, f"Details: {response.json()}"
    data = response.json()
    assert isinstance(data, dict)

    assert isinstance(data["TableNames"], dict)
    assert isinstance(data["Menu"], dict)


@pytest.mark.asyncio
async def test_update_products(client: AsyncClient):
    response = await client.put(
        url=f'/products/update/{tables[0]}/1',
        json=update_data,
        auth=auth
    )

    assert response.status_code == 200, f"Details: {response.json()}"
    response_updated_data_ = response.json()
    assert response_updated_data_['name'] == update_data['name']
    assert response_updated_data_['description'] == update_data['description']
    assert response_updated_data_['price'] == update_data['price']


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient):
    response = await client.delete(
        url=f'/products/delete/{tables[0]}/1',
        auth=auth
    )

    assert response.status_code == 200, f"Details: {response.json()}"
    data = response.json()
    assert isinstance(data, str)
