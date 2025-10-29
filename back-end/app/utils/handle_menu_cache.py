import asyncio
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

warsaw_tz = ZoneInfo("Europe/Warsaw")


@dataclass
class MenuCache:
    _menu_cache_data: dict | None = None
    _menu_cache_expire: datetime | None = None


cacheMenu = MenuCache(None, None)


async def set_menu_cache(data: dict):
    cacheMenu._menu_cache_data = data
    cacheMenu._menu_cache_expire = datetime.now(
        warsaw_tz) + timedelta(minutes=5)
    return cacheMenu._menu_cache_data


async def get_menu_cache():
    return cacheMenu._menu_cache_data


async def is_cache_expired():
    if not cacheMenu._menu_cache_data or cacheMenu._menu_cache_expire <= datetime.now(warsaw_tz):
        return True
    else:
        return False


async def delete_menu_cache():
    cacheMenu._menu_cache_data = None
    cacheMenu._menu_cache_expire = None
