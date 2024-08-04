from typing import Annotated

from fastapi import Depends, status

from app.api import routes
from app.api.models import Report, Token
from app.external.clients import clients


@routes.auth.post('/login')
def authenticate(
    token: Annotated[Token, Depends(clients.auth_client.authenticate)],
) -> Token:
    """Аутентифицирует пользователя."""
    return token


@routes.auth.post('/register')
def register(
    token: Annotated[Token, Depends(clients.auth_client.register)],
) -> Token:
    """Регистрирует пользователя."""
    return token


@routes.auth.post('/verify')
def verify(
    message: Annotated[dict[str, str], Depends(clients.auth_client.verify)],
) -> dict[str, str]:
    """Верифицирует пользователя."""
    return message


@routes.transaction.post('/transaction', status_code=status.HTTP_201_CREATED)
def create_transaction(
    message: Annotated[dict[str, str], Depends(clients.transactions_client.create_transaction)],  # noqa: E501 anotation
) -> dict[str, str]:
    """Регистрирует пользователя."""
    return message


@routes.transaction.post('/report')
def create_report(
    report: Annotated[Report, Depends(clients.transactions_client.get_report)],
) -> Report:
    """Регистрирует пользователя."""
    return report
