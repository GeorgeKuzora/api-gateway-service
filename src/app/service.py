import logging

from fastapi import FastAPI

from app.api import routes


def main() -> None:
    """Точка входа в программу."""
    app = FastAPI()
    app.include_router(router=routes.auth)
    app.include_router(router=routes.register)
    app.include_router(router=routes.transaction)
    app.include_router(router=routes.report)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info(main())
