from collections import namedtuple
from datetime import datetime
from enum import IntEnum
from typing import Self

from pydantic import BaseModel, Field, field_serializer, model_validator

ValidationRules = namedtuple(
    'ValidationRules',
    [
        'username_max_len',
        'password_max_len',
        'password_min_len',
    ],
)

validation_rules = ValidationRules(
    username_max_len=50,  # noqa: WPS432 not magic
    password_max_len=100,
    password_min_len=8,
)


class UserCredentials(BaseModel):
    """Данные аутентификации пользователя."""

    username: str = Field(
        title='Имя пользователя',
        max_length=validation_rules.username_max_len,
    )
    password: str = Field(
        title='Пароль пользователя',
        max_length=validation_rules.password_max_len,
        min_length=validation_rules.password_min_len,
    )


class Token(BaseModel):
    """Токен пользователя."""

    token: str


class TransactionType(IntEnum):
    """
    Тип транзакции.

    Может быть либо Продажа, либо Покупка.
    """

    deposit = 0
    withdraw = 1


class Transaction(BaseModel):
    """Транзакция выполненная пользователем."""

    username: str = Field(
        title='Имя пользователя',
        max_length=validation_rules.username_max_len,
    )
    amount: int = Field(title='Размер транзакции', gt=0)
    transaction_type: TransactionType = Field(title='Тип транзакции')
    timestamp: datetime = Field(
        title='Дата совершения транзакции',
    )

    @field_serializer('timestamp', when_used='always')
    def serialize_timestamp_to_iso_format(self, timestamp: datetime):
        """Сериализирует поле timestamp в isoformat."""
        return timestamp.isoformat()


class ReportRequest(BaseModel):
    """Запрос на получения отчета."""

    username: str = Field(
        title='Имя пользователя',
        max_length=validation_rules.username_max_len,
    )
    start_date: datetime = Field(
        title='Дата начала периода',
    )
    end_date: datetime = Field(
        title='Дата конца периода',
    )

    @model_validator(mode='after')
    def check_dates_match(self) -> Self:
        """Проверяет что даты соответствуют друг другу."""
        if self.start_date > self.end_date:
            raise ValueError('дата начала периода больше даты конца периода')
        return self

    @field_serializer('start_date', 'end_date', when_used='always')
    def serialize_datetime_to_iso_format(self, timestamp: datetime):
        """Сериализирует поля start_date, end_date в isoformat."""
        return timestamp.isoformat()


class Report(BaseModel):
    """Отчет о транзакциях."""

    request: ReportRequest = Field(title='Параметры запрошенного отчета')
    transactions: list[Transaction] = Field(title='Список транзакций')
