from typing import Annotated

from fastapi import Depends, status

from app.api import routes
from app.api.models import Report, Token
from app.external.clients import clients


@routes.auth.post('/login')
def authenticate(
    token: Annotated[Token, Depends(clients.auth_client.authenticate)],
) -> Token:
    """
    Аутентифицирует пользователя.

    Валидирует данные пользователя,
    создает и возвращает токен пользователя.

    :param token: Токен получаемый от клиента сервиса auth.
    :type token: Token
    :return: Токен пользователя.
    :rtype: Token
    """
    return token


@routes.auth.post('/register')
def register(
    token: Annotated[Token, Depends(clients.auth_client.register)],
) -> Token:
    """
    Регистрирует пользователя.

    Регистрирует пользователя в системе,
    создает и возвращает токен пользователя.

    :param token: Токен получаемый от клиента сервиса auth.
    :type token: Token
    :return: Токен пользователя.
    :rtype: Token
    """
    return token


@routes.auth.post(
    '/verify', dependencies=[Depends(clients.auth_client.check_token)],
)
def verify(
    message: Annotated[dict[str, str], Depends(clients.auth_client.verify)],
) -> dict[str, str]:
    """
    Верифицирует пользователя.

    Валидирует токен пользователя,
    загружает изображение пользователя.

    :param message: Сообщение о успешности операции.
    :type message: dict[str, str]
    :return: Сообщение о успешности операции.
    :rtype: dict[str, str]
    """
    return message


@routes.transaction.post('/transaction', status_code=status.HTTP_201_CREATED)
def create_transaction(
    message: Annotated[dict[str, str], Depends(clients.transactions_client.create_transaction)],  # noqa: E501 annotation
) -> dict[str, str]:
    """
    Создает транзакцию.

    :param message: Сообщение о успешности операции.
    :type message: dict[str, str]
    :return: Сообщение о успешности операции.
    :rtype: dict[str, str]
    """
    return message


@routes.transaction.post('/report')
def create_report(
    report: Annotated[Report, Depends(clients.transactions_client.get_report)],
) -> Report:
    """
    Создает отчет о транзакциях.

    Создает и возвращает отчет о транзакциях.

    :param report: Отчет о транзакциях созданный клиентом сервиса транзакций.
    :type report: Report
    :return: Отчет о транзакциях.
    :rtype: Report
    """
    return report
