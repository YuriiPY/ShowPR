import asyncio
from aiogram.types import Message


async def delayed_delete_message(message: Message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        print(f'Error to delete msg:\n {message.__dict__}\n {str(e)}')
