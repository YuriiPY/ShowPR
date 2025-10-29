import asyncio
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


@dataclass
class Store:
    status: bool
    change_at: datetime
    until: str | None = None


warsaw_tz = ZoneInfo("Europe/Warsaw")

store_status = Store(status=True, change_at=datetime.now(warsaw_tz))

_status_lock = asyncio.Lock()


async def set_store_status_data(status: bool, until: str | None = None):
    async with _status_lock:
        store_status.status = status
        store_status.until = until
        store_status.change_at = datetime.now(timezone.utc)
        return store_status.status


async def get_store_status_data() -> dict:
    async with _status_lock:
        return asdict(store_status)
