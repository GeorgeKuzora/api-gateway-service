import logging

from fastapi import Depends

from app.api.routes import healthz
from app.external.clients import clients

logger = logging.getLogger(__name__)


ready_message = {'message': 'service is ready'}
up_message = {'message': 'service is up'}


@healthz.get('/up')
async def up_check() -> dict[str, str]:
    """Healthcheck для сервера сервиса."""
    return up_message


@healthz.get(
    '/ready',
    dependencies=[
        Depends(clients.auth_client.is_ready),
        Depends(clients.transactions_client.is_ready),
    ],
)
async def ready_check() -> dict[str, str]:
    """Healthcheck для зависимостей приложения."""
    return ready_message
