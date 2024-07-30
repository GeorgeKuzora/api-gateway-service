import logging

from fastapi import FastAPI

# whithout import from handlers routing doesn't work
from app.api.handlers import routes  # type: ignore

app = FastAPI()
app.include_router(router=routes.auth)
app.include_router(router=routes.transaction)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
