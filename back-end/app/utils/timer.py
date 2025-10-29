import asyncio
import datetime


async def timer(func, time: str, *args, **kwargs):
    now = datetime.datetime.now()

    target_time = datetime.datetime.strptime(time, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )

    if target_time <= now:
        target_time += datetime.timedelta(days=1)

    seconds_left = (target_time - now).total_seconds()
    print(
        f"Sleeping {seconds_left:.2f} seconds until {target_time}| function {func.__name__}| {seconds_left}")

    await asyncio.sleep(seconds_left)

    print("🔄The delayed function is starting ...")

    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    else:
        return await func(*args, **kwargs)
