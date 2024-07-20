from typing import Annotated

from fastapi import Depends, status

from app.api import routes
from app.api.models import Report, Token
from app.external.clients import clients

root = '/'


@routes.auth.post(root)
async def authenticate(
    token: Annotated[Token, Depends(clients.auth_client.authenticate)],
) -> Token:
    """Аутентифицирует пользователя."""
    return token


@routes.register.post(root)
async def register(
    token: Annotated[Token, Depends(clients.auth_client.register)],
) -> Token:
    """Регистрирует пользователя."""
    return token


@routes.transaction.post(root, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    message: Annotated[dict[str, str], Depends(clients.transactions_client.create_transaction)],
):
    """Регистрирует пользователя."""
    return message


@routes.report.post(root)
async def create_report(
    report: Annotated[Report, Depends(clients.transactions_client.get_report)],
):
    """Регистрирует пользователя."""
    return report
