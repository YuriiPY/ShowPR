import asyncio
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.store import StoreTimePayload
from app.utils.timer import timer
from app.utils.handle_store import set_store_status_data, get_store_status_data
from app.api.security.admin_auth import admin_auth


router = APIRouter(
    prefix='/store'
)

scheduled_task = None


@router.post('/close', dependencies=[Depends(admin_auth)])
async def close_store(
    payload: StoreTimePayload
):
    global scheduled_task

    if scheduled_task and not scheduled_task.done():
        scheduled_task.cancel()
        print("🛑 Cancelling previous task")
        try:
            await scheduled_task
        except asyncio.CancelledError:
            print("✔ Previous task cancelled")

    updated_store_status = await set_store_status_data(status=False, until=payload.until)

    if payload.until:

        if ":" not in payload.until:
            raise HTTPException(
                status_code=400, detail=f"Invalid payload: time data '{payload.until}' does not match format %H:%M")
        print(
            f"❌Store closed \nDetails:\n Store_status: {updated_store_status} \n Closed until {payload}")
        scheduled_task = asyncio.create_task(
            timer(func=set_store_status_data, time=payload.until, status=True))

        return {"message": "Store closed now", "status": updated_store_status}

    elif payload.close_now:
        print(
            f"❌Store closed immediately \nDetails:\n Store_status: {updated_store_status}")
        return {"message": "Store closed immediately", "status": updated_store_status}

    raise HTTPException(
        status_code=400, detail="Invalid payload: provide either close_now or until")


@router.post('/open', dependencies=[Depends(admin_auth)])
async def open_store():
    global scheduled_task

    if scheduled_task and not scheduled_task.done():
        scheduled_task.cancel()
        print("🛑 Cancelling previous task")
        try:
            await scheduled_task
        except asyncio.CancelledError:
            print("✔ Previous task cancelled")

    updated_store_status = await set_store_status_data(True)
    print(f"✅Store open \nDetails: {updated_store_status}")

    return {"message": "Store open", "status": updated_store_status}


@router.get('/status')
async def get_store_status():
    store_status = await get_store_status_data()
    return {
        "isOpen": store_status.get("status"),
        "until": store_status.get("until"),
        "changedAt": store_status.get("change_at")
    }
