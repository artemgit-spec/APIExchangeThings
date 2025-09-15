import uvicorn
from fastapi import FastAPI

from routers.admin import router_admin
from routers.users import router_user
from routers.things import router_thing
from routers.deal import router_deal
from core.security import router_auth

from db.initial_data import init_info_db


async def start_event(app: FastAPI):
    await init_info_db()
    yield


app = FastAPI(lifespan=start_event)
app.include_router(router_auth)
app.include_router(router_admin)
app.include_router(router_user)
app.include_router(router_thing)
app.include_router(router_deal)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
