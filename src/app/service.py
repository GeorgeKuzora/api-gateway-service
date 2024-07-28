import logging

from fastapi import FastAPI

from app.api import routes

app = FastAPI()


app.include_router(router=routes.auth)
app.include_router(router=routes.transaction)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
