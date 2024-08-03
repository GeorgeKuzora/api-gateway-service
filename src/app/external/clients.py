import logging
from collections import namedtuple
from dataclasses import dataclass
from enum import StrEnum
from typing import Annotated, Any

import httpx
from fastapi import Header, status

from app.api.models import (
    Report,
    ReportRequest,
    Token,
    Transaction,
    UserCredentials,
)
from app.system import errors
from config.config import get_settings

logger = logging.getLogger(__name__)

good_response = {'message': 'ok'}


class Key(StrEnum):
    """Часто повторяемые ключи."""

    encoded_token = 'encoded_token'  # noqa: S105 key
    authorization = 'Authorization'
    transactions = 'transactions'
    http_protocol_prefix = 'http://'
    https_protocol_prefix = 'https://'


@dataclass
class Client:
    """Клиент библиотеки для формирования HTTP запросов."""

    client: httpx.AsyncClient = httpx.AsyncClient()

    async def get(self, *args, **kwargs) -> Any:
        """Метод GET."""
        return await self.client.get(*args, **kwargs)

    async def post(self, *args, **kwargs) -> Any:
        """Метод POST."""
        return await self.client.post(*args, **kwargs)


class AuthServiceClient:
    """Клиент для доступа к сервису аутентификации."""

    def __init__(self, client: Client) -> None:
        """Метод инициализации."""
        settings = get_settings()
        self.host = settings.auth_host
        self.port = settings.auth_port
        self.client = client

    async def register(self, user_creds: UserCredentials) -> Token:
        """
        Метод аутентификации пользователя.

        :param user_creds: Данные авторизации пользователя.
        :type user_creds: UserCredentials
        :return: Токен пользователя
        :rtype: Token
        :raises ServerError: В случае плохого ответа сервиса
        :raises UnprocessableError: В случае неверного формата запроса
        """
        url = f'{Key.http_protocol_prefix}{self.host}:{self.port}/register'
        resp = await self.client.post(
            url, json=user_creds.model_dump(),
        )
        if resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            logger.error(
                f'{url} {status.HTTP_422_UNPROCESSABLE_ENTITY}',  # noqa: E501
            )
            raise errors.UnprocessableError()
        if resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            logger.error(
                f'{url} {status.HTTP_500_INTERNAL_SERVER_ERROR}',  # noqa: E501
            )
            raise errors.ServerError()
        return Token(token=resp.json().get(Key.encoded_token, ''))

    async def authenticate(
        self,
        user_creds: UserCredentials,
        authorization: Annotated[str | None, Header()] = None,
    ) -> Token:
        """
        Метод аутентификации пользователя.

        :param user_creds: Данные авторизации пользователя.
        :type user_creds: UserCredentials
        :param authorization: токен пользователя
        :type authorization: str
        :return: Токен пользователя
        :rtype: Token
        :raises NotFoundError: данные не найдены
        :raises UnauthorizedError: неавторизирован
        :raises ServerError: ошибка сервера
        """
        url = f'{Key.http_protocol_prefix}{self.host}:{self.port}/login'
        headers = {Key.authorization: authorization}
        resp = await self.client.post(
            url,
            json=user_creds.model_dump(),
            headers=headers,
        )
        if resp.status_code == status.HTTP_401_UNAUTHORIZED:
            logger.error(
                f'{url} {status.HTTP_401_UNAUTHORIZED}',
            )
            raise errors.UnauthorizedError()
        elif resp.status_code == status.HTTP_404_NOT_FOUND:
            logger.error(
                f'{url} {status.HTTP_404_NOT_FOUND}',
            )
            raise errors.NotFoundError()
        elif resp.status_code == status.HTTP_200_OK:
            payload = resp.json()
            return Token(token=payload.get(Key.encoded_token))

        logger.error(
            f'{url} {status.HTTP_500_INTERNAL_SERVER_ERROR}',
        )
        raise errors.ServerError()

    async def check_token(
        self, authorization: Annotated[str, Header()],
    ) -> None:
        """
        Валидирует токен пользователя.

        :param authorization: Заголовок с токеном пользователя
        :type authorization: str
        :raises NotFoundError: данные не найдены
        :raises UnauthorizedError: неавторизирован
        :raises ServerError: ошибка сервера
        """
        url = f'{Key.http_protocol_prefix}{self.host}:{self.port}/check_token'
        headers = {str(Key.authorization): authorization}
        resp = await self.client.post(
            url=url,
            headers=headers,
        )
        if resp.status_code == status.HTTP_404_NOT_FOUND:
            logger.info(f'{url} токен не найден')
            raise errors.NotFoundError()
        elif resp.status_code == status.HTTP_401_UNAUTHORIZED:
            logger.info(f'{url} токен не валиден')
            raise errors.UnauthorizedError()
        elif resp.status_code == status.HTTP_200_OK:
            logger.debug(f'{url}токен валиден')
        else:
            logger.error(f'{url} ошибка сервера')
            raise errors.ServerError()


class TransactionServiceClient:
    """Клиент сервиса транзакций."""

    def __init__(self, client: Client) -> None:
        """Метод инициализации."""
        settings = get_settings()
        self.host = settings.transactions_host
        self.port = settings.transactions_port
        self.client = client

    async def get_report(
        self,
        report_request: ReportRequest,
    ) -> Report:
        """
        Запрашивает отчет о транзакциях.

        :param report_request: Данные для запроса отчета
        :type report_request: ReportRequest
        :return: Отчет о транзакциях
        :rtype: Report
        :raises ServerError: Ошибка доступа
        """
        url = f'{Key.http_protocol_prefix}{self.host}:{self.port}/create_report'
        resp = await self.client.post(
            url=url,
            json=report_request.model_dump(),
        )
        if resp.status_code == status.HTTP_200_OK:
            payload: dict[str, str | int] = resp.json()
            return self._make_report(payload, report_request)

        logger.error(f'{url} ошибка сервера')
        raise errors.ServerError()

    async def create_transaction(
        self, transaction: Transaction,
    ) -> dict[str, str]:
        """
        Создает транзакцию на основании данных пользователя.

        :param transaction: Транзакция совершенная пользовалетем.
        :type transaction: Transaction
        :return: Сообщение о успехе
        :rtype: dict[str, str]
        :raises ServerError: При плохом ответе от сервиса
        """
        url = f'{Key.http_protocol_prefix}{self.host}:{self.port}/create_transaction'  # noqa: E501 can't make shorter
        resp = await self.client.post(
            url=url,
            json=transaction.model_dump(),
        )
        if resp.status_code == status.HTTP_201_CREATED:
            logger.debug(f'транзакция создана: {transaction}')
            return good_response
        logger.error(f'{url} ошибка при создании транзации')
        raise errors.ServerError()

    def _make_report(self, payload, request) -> Report:
        trasactions = self._make_transactions(payload.get(Key.transactions))
        report = Report(
            request=request, transactions=trasactions,
        )
        logger.debug(f'Отчет получен: {report}')
        return report

    def _make_transactions(
        self, transactions: list[dict] | None,  # type: ignore
    ) -> list[Transaction]:
        if transactions is None:
            raise ValueError('expected list but recieved None')
        result_transactions = []
        for key_value in transactions:
            result_transactions.append(Transaction(**key_value))
        return result_transactions


Clients = namedtuple(
    'Clients',
    ['auth_client', 'transactions_client'],
)

clients = Clients(
    auth_client=AuthServiceClient(Client()),
    transactions_client=TransactionServiceClient(Client()),
)
