from fastapi import FastAPI

from breeze_bot.app.deps import Container
from breeze_bot.app.routers import router

app = FastAPI()

app.container = Container()
app.include_router(router)
