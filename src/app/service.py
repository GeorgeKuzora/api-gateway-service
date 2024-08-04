import logging

from fastapi import FastAPI

# whithout import from handlers routing doesn't work
from app.api.handlers import routes  # type: ignore
from app.api.healthz.handlers import healthz  # type: ignore

app = FastAPI()
app.include_router(router=routes.auth)
app.include_router(router=routes.transaction)
app.include_router(router=healthz)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
