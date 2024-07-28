from fastapi import HTTPException, status


class ServerError(HTTPException):
    """Ошибка при ответе сервера 500."""

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = 'Неизвестная ошибка сервера',
    ):
        """
        Метод инициализации.

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
        Метод инициализации.

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
        Метод инициализации.

        :param status_code: Код ответа
        :type status_code: int
        :param detail: Сообщение
        :type detail: str
        """
        self.status_code = status_code
        self.detail = detail
