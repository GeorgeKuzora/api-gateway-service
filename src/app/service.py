import logging

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

# whithout import from handlers routing doesn't work
from app.api.handlers import routes  # type: ignore
from app.api.healthz.handlers import healthz  # type: ignore
from app.metrics.tracing import tracing_middleware

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=tracing_middleware)

app.include_router(router=routes.auth)
app.include_router(router=routes.transaction)
app.include_router(router=healthz)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
