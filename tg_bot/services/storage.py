import os
import base64
from typing import Optional, Tuple, Union
import aiofiles
import httpx

import core.config as config


# async def save_photo(file_data: bytes, file_id: str) -> Union[str, bool]:
#     try:
#         image_bytes = base64.b64decode(file_data)

#         os.makedirs(config.STORAGE_PHOTO_PATH, exist_ok=True)
#         file_path = os.path.join(config.STORAGE_PHOTO_PATH, f"{file_id}.png")

#         async with aiofiles.open(file_path, "wb") as file:
#             await file.write(image_bytes)

#         if not os.path.exists(file_path) and (file_size := os.path.getsize) == 0:
#             print("ERROR: ", "FILE_PATH", file_path, "FILE_SIZE", file_size)
#             return False

#         return file_path

#     except Exception as e:
#         print(str(e))
#         return False

# response = await client.post(
#     f'http://localhost:8000/products/create?table={table}',
#     json=item_fields
# )
#   print('request')

#    if response.status_code == 200:
#         print('response')
#         return {"func_status": "Product successfully created!"}
#     else:
#         print(response.text)
#         return {"func_status": 'Failed to create a new item', 'detail': response.text}


async def save_photo(data: bytes, name: str):
    try:

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.imgbb.com/1/upload?key={config.IMGBB_API_KEY}",
                data={"name": name},
                files={"image": data}
            )

            if response.status_code == 200:
                res_data = response.json()
                img_url = res_data.get("data", {}).get("url")
                print(response, img_url)
                return img_url

    except Exception as e:
        print(str(e))


async def delete_photo(file_id: str) -> bool:
    file_path = config.STORAGE_PHOTO_PATH + str(file_id) + '.png'
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        else:
            print(f"File: {file_path} not found!")
            return False
    except Exception as e:
        print(str(e))
        return False
