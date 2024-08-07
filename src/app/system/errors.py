import logging

from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class ServerError(HTTPException):
    """Ошибка при ответе сервера 500."""

    def __init__(
        self,
        status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE,
        detail: str = 'Неизвестная ошибка сервера',
    ):
        """
        Метод инициализации ServerError.

        :param status_code: Код ответа
        :type status_code: int
        :param detail: Сообщение
        :type detail: str
        """
        self.status_code = status_code
        self.detail = detail


class UnauthorizedError(HTTPException):
    """Ошибка при ответе сервера 401."""

    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = 'Ошибка авторизации пользователя',
    ):
        """
        Метод инициализации UnauthorizedError.

        :param status_code: Код ответа
        :type status_code: int
        :param detail: Сообщение
        :type detail: str
        """
        self.status_code = status_code
        self.detail = detail


class NotFoundError(HTTPException):
    """Ошибка при ответе сервера 401."""

    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = 'Запрошенные данные не найдены',
    ):
        """
        Метод инициализации NotFoundError.

        :param status_code: Код ответа
        :type status_code: int
        :param detail: Сообщение
        :type detail: str
        """
        self.status_code = status_code
        self.detail = detail


class UnprocessableError(HTTPException):
    """Ошибка при ответе сервера 422."""

    def __init__(
        self,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail: str = 'Запрос имеет неверный формат',
    ):
        """
        Метод инициализации UnprocessableError.

        :param status_code: Код ответа
        :type status_code: int
        :param detail: Сообщение
        :type detail: str
        """
        self.status_code = status_code
        self.detail = detail


http_errors = {
    status.HTTP_422_UNPROCESSABLE_ENTITY: UnprocessableError,
    status.HTTP_404_NOT_FOUND: NotFoundError,
    status.HTTP_503_SERVICE_UNAVAILABLE: ServerError,
    status.HTTP_500_INTERNAL_SERVER_ERROR: ServerError,
    status.HTTP_401_UNAUTHORIZED: UnauthorizedError,
}

good_status_codes = [
    status.HTTP_200_OK,
    status.HTTP_201_CREATED,
]


def handle_status_code(status_code: int):
    """Проверяет код ответа поднимает исключение при плохом коде ответа."""
    if status_code not in good_status_codes:
        logger.error(f'Recived bad status code {status_code}')
        raise http_errors.get(status_code, ServerError)()


def handle_healthz_status_code(status_code: int):
    """Проверяет код ответа поднимает исключение при плохом коде ответа."""
    if status_code != status.HTTP_200_OK:
        logger.error(f'Recived bad status code {status_code}')
        raise ServerError()
