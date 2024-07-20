import logging
from collections import namedtuple
from typing import Annotated

import aiohttp
from fastapi import Depends, Header, status
from fastapi.exceptions import HTTPException

from app.api.models import (
    Report,
    ReportRequest,
    Token,
    Transaction,
    UserCredentials,
)

logger = logging.getLogger(__name__)
session = aiohttp.ClientSession()


class AuthServiceClient:
    """Клиент для доступа к сервису аутентификации."""

    def __init__(self) -> None:
        """Метод инициализации."""
        self.host = 'host'
        self.port = 'port'

    async def register(self, user_creds: UserCredentials) -> Token:
        """
        Метод аутентификации пользователя.

        :param user_creds: Данные авторизации пользователя.
        :type user_creds: UserCredentials
        :return: Токен пользователя
        :rtype: Token
        :raises HTTPException: В случае плохого ответа сервиса
        """
        async with session.post(
            f'{self.host}:{self.port}', json=user_creds.model_dump_json(),
        ) as resp:
            if resp.status == status.HTTP_500_INTERNAL_SERVER_ERROR:
                logger.error(
                    f'{self.host}:{self.port} respose status {status.HTTP_500_INTERNAL_SERVER_ERROR}',  # noqa
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            payload = await resp.json()
            return Token(token=payload.get('token'))

    async def authenticate(
        self,
        user_creds: UserCredentials,
        authorization: Annotated[str, Header()],
    ) -> Token:
        """
        Метод аутентификации пользователя.

        :param user_creds: Данные авторизации пользователя.
        :type user_creds: UserCredentials
        :param authorization: токен пользователя
        :type authorization: str
        :return: Токен пользователя
        :rtype: Token
        :raises HTTPException: В случае плохого ответа сервиса
        """
        headers = {'Authorization:': authorization}
        async with session.post(
            f'{self.host}:{self.port}',
            json=user_creds.model_dump_json(),
            headers=headers,
        ) as resp:
            if resp.status == status.HTTP_401_UNAUTHORIZED:
                logger.error(
                    f'{self.host}:{self.port} respose status {status.HTTP_401_UNAUTHORIZED}',  # noqa
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
            elif resp.status == status.HTTP_404_NOT_FOUND:
                logger.error(
                    f'{self.host}:{self.port} respose status {status.HTTP_404_NOT_FOUND}',  # noqa
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            elif resp.status == status.HTTP_200_OK:
                payload = await resp.json()
                return Token(token=payload.get('token'))

            logger.error(
                f'{self.host}:{self.port} respose status {status.HTTP_500_INTERNAL_SERVER_ERROR}',  # noqa
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def check_token(
        self, authorization: Annotated[str, Header()],
    ) -> None:
        """
        Валидирует токен пользователя.

        :param authorization: Заголовок с токеном пользователя
        :type authorization: str
        :raises HTTPException: Ошибка доступа
        """
        headers = {'Authorization:': authorization}
        async with session.post(
            f'{self.host}:{self.port}',
            headers=headers,
        ) as resp:
            if resp.status == status.HTTP_404_NOT_FOUND:
                logger.info('токен не найден')
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            elif resp.status == status.HTTP_401_UNAUTHORIZED:
                logger.info('токен не валиден')
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED1)
            elif resp.status == status.HTTP_200_OK:
                logger.debug('токен валиден')

            logger.error('неизвестная ошибка сервера')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TransactionServiceClient:
    """Клиент сервиса транзакций."""

    def __init__(self) -> None:
        """Метод инициализации."""
        self.host = 'host'
        self.port = 'port'

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
        :raises HTTPException: Ошибка доступа
        """
        async with session.get(
            f'{self.host}:{self.port}',
            json=report_request.model_dump_json(),
        ) as resp:
            if resp.status == status.HTTP_200_OK:
                payload: dict = await resp.json()
                request = payload.get('request')
                transactions = payload.get('transactions')
                if request is not None and transactions is not None:
                    request = ReportRequest(**request)
                    report = Report(request=request, transactions=transactions)
                else:
                    logger.error('Ошибка при получении отчета')
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                logger.debug(f'Отчет получен: {report}')
                return report

            logger.error('неизвестная ошибка сервера')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def create_transaction(
        self, transaction: Transaction,
    ) -> dict[str, str]:
        async with session.post(
            f'{self.host}:{self.port}',
            json=transaction.model_dump_json(),
        ) as resp:
            if resp.status == status.HTTP_201_CREATED:
                logger.debug(f'транзакция создана: {transaction}')
                return {'message': 'transaction created'}
            logger.error('Ошибка при получении отчета')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


Clients = namedtuple(
    'Clients',
    ['auth_client', 'transactions_client'],
)

clients = Clients(
    auth_client=AuthServiceClient(),
    transactions_client=TransactionServiceClient(),
)
