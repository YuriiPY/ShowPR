import pytest
import asyncio
import pytest_asyncio
from httpx import AsyncClient

from app.db.seeds import order_payload, location_data, order_data


@pytest.mark.asyncio
async def test_get_amount(client: AsyncClient):
    response = await client.post(
        url='/order/get_amount',
        json=order_payload
    )

    assert response.status_code == 200, f"Details: {response.json()}"
    data = response.json()
    assert isinstance(data["products"], dict)
    assert isinstance(data["totalAmount"], (int, float))


# @pytest.mark.asyncio
# async def test_get_location(client: AsyncClient):
#     response = await client.post(
#         url='/order/get_location',
#         json=location_data
#     )

#     assert response.status_code == 200, f"Details: {response.json()}"
#     data = response.json()
#     assert data["street"]


@pytest.mark.asyncio
async def test_add_order(client: AsyncClient):
    response = await client.post(
        url='/order/add_order',
        json=order_data
    )

    assert response.status_code == 200, f"Details: {response.json()}"
    data = response.json()
    assert data['name'] == order_data['name']
    assert data['phone_number'] == order_data['phone_number']
    assert data['email'] == order_data['email']
    assert data['delivery_time']
    assert data['delivery_date']
    assert isinstance(data['total_amount'], (int, float))
    assert isinstance(data['items'], list) and len(data['items']) > 0
