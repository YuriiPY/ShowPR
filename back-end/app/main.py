import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import products, order, store
from app.core.config import FRONT_END_URL, BACKEND_HOST, BACKEND_PORT, NGINX_URL
from app.db.session import database_connection_test

app = FastAPI()

app.include_router(products.router)
app.include_router(order.router)
app.include_router(store.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONT_END_URL,
        NGINX_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def on_startup():
    await database_connection_test()


if __name__ == "__main__":
    app.add_event_handler("startup", on_startup)

    uvicorn.run(app, host=BACKEND_HOST, port=BACKEND_PORT)
