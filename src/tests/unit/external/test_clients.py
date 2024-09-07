from datetime import datetime
from enum import StrEnum

import pytest
from fastapi import HTTPException, status

from app.api.models import (
    Report,
    ReportRequest,
    Token,
    Transaction,
    TransactionType,
    UserCredentials,
)
from app.external.clients import (
    AuthServiceClient,
    TransactionServiceClient,
    good_response,
)


class Keys(StrEnum):
    """Используемые ключи для словарей."""

    encoded_token = 'encoded_token'  # noqa: S105 test data
    authorization = 'Authorization'
    status = 'status'
    json = 'json'
    status_code = 'status_code'


test_user_creds = UserCredentials(  # noqa: S106 test data
    username='test_user1',
    password='test_password1',
)
test_encoded_token = 'test_encoded_token'  # noqa: S105 test data
test_token_object = {Keys.encoded_token: test_encoded_token}
test_headers = {Keys.authorization: f'Bearer {test_encoded_token}'}


class TestRegister:
    """Тестирует метод register."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'user_creds, client_builder, expected_status',
        (
            pytest.param(
                test_user_creds,
                'client',
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                id='response status 500',
            ),
        ),
    )
    async def test_not_valid_responses(
        self, user_creds, client_builder, expected_status, request,
    ):
        """Тестирует статусы ошибок ответа."""
        client_builder = request.getfixturevalue(client_builder)
        client = client_builder(
            status_code=expected_status,
        )
        auth_client = AuthServiceClient(client)

        with pytest.raises(HTTPException):
            await auth_client.register(user_creds)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'user_creds, client_builder, expected',
        (
            pytest.param(
                test_user_creds,
                'client',
                {
                    Keys.status: status.HTTP_200_OK,
                    Keys.json: test_token_object,
                },
                id='response status 200 valid json',
            ),
        ),
    )
    async def test_valid_response(
        self, user_creds, client_builder, expected, request,
    ):
        """Тестирует статус и тело ответа."""
        client_builder = request.getfixturevalue(client_builder)
        client = client_builder(
            status_code=expected[Keys.status],
            json=expected[Keys.json],
        )
        auth_client = AuthServiceClient(client)

        response: Token = await auth_client.register(user_creds)

        assert response.token == expected[Keys.json][Keys.encoded_token]


class TestAuthenticate:
    """Тестирует метод authenticate."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'user_creds, headers, expected_status',
        (
            pytest.param(
                test_user_creds,
                test_headers,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                id='response status 500',
            ),
            pytest.param(
                test_user_creds,
                test_headers,
                status.HTTP_401_UNAUTHORIZED,
                id='response status 401',
            ),
            pytest.param(
                test_user_creds,
                test_headers,
                status.HTTP_404_NOT_FOUND,
                id='response status 404',
            ),
        ),
    )
    async def test_not_valid_status_codes(
        self, user_creds, headers, expected_status, client,
    ):
        """Тестирует неверные ответы клиента."""
        client = client(
            status_code=expected_status,
        )
        auth_client = AuthServiceClient(client)

        with pytest.raises(HTTPException):
            await auth_client.authenticate(
                user_creds, headers[Keys.authorization],
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'user_creds, headers, expected',
        (
            pytest.param(
                test_user_creds,
                test_headers,
                {
                    Keys.status: status.HTTP_200_OK,
                    Keys.json: test_token_object,
                },
                id='response status 200 valid json',
            ),
        ),
    )
    async def test_valid_response(
        self, user_creds, headers, expected, client,
    ):
        """Тестирует статут и тело ответа."""
        client = client(
            status_code=expected[Keys.status],
            json=expected[Keys.json],
            headers=headers,
        )
        auth_client = AuthServiceClient(client)

        response: Token = await auth_client.authenticate(
            user_creds, headers[Keys.authorization],
        )

        assert response.token == expected[Keys.json][Keys.encoded_token]


class TestCheckToken:
    """Тестирует метод check_token."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'headers, expected_status',
        (
            pytest.param(
                test_headers,
                status.HTTP_200_OK,
                id='response status 200',
            ),
            pytest.param(
                test_headers,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                id='response status 500',
                marks=pytest.mark.xfail(raises=HTTPException),
            ),
            pytest.param(
                test_headers,
                status.HTTP_401_UNAUTHORIZED,
                id='response status 401',
                marks=pytest.mark.xfail(raises=HTTPException),
            ),
            pytest.param(
                test_headers,
                status.HTTP_404_NOT_FOUND,
                id='response status 404',
                marks=pytest.mark.xfail(raises=HTTPException),
            ),
        ),
    )
    async def test_status_codes(
        self, headers, expected_status, client,
    ):
        """Тестирует неверные ответы клиента."""
        client = client(
            status_code=expected_status,
        )
        auth_client = AuthServiceClient(client)

        await auth_client.check_token(headers[Keys.authorization])


class TestGetReport:
    """Тестирует метод get_report."""

    username = 'george'
    start_date = datetime(year=2024, month=1, day=1)  # noqa: WPS432 test value
    end_date = datetime(year=2024, month=1, day=30)  # noqa: WPS432 test value

    test_request = ReportRequest(
        username=username, start_date=start_date, end_date=end_date,
    )
    test_transaction = {
        'username': username,
        'amount': 1,
        'transaction_type': 1,
        'timestamp': datetime(year=2024, month=1, day=15),  # noqa: WPS432, E501 test value
        'transaction_id': 1,
    }
    expected_response = {
        'report_id': 1,
        'user_id': username,
        'start_date': start_date,
        'end_date': end_date,
        'transactions': [test_transaction],
    }
    invalid_transactions = {
        'report_id': 1,
        'user_id': username,
        'start_date': start_date,
        'end_date': end_date,
        'transactions': None,
    }

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'report_request, expected',
        (
            pytest.param(
                test_request,
                {
                    Keys.json: expected_response,
                    Keys.status_code: status.HTTP_200_OK,
                },
                id='valid response 200',
            ),
            pytest.param(
                test_request,
                {
                    Keys.json: invalid_transactions,
                    Keys.status_code: status.HTTP_200_OK,
                },
                id='response 200 invalid transactions',
                marks=pytest.mark.xfail(raises=ValueError),
            ),
            pytest.param(
                test_request,
                {
                    Keys.json: {},
                    Keys.status_code: status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                id='response 500',
                marks=pytest.mark.xfail(raises=HTTPException),
            ),
        ),
    )
    async def test_get_report(self, report_request, expected, client):
        """Тестирует ответ и тело ответа."""
        client = client(
            status_code=expected[Keys.status_code],
            json=expected[Keys.json],
        )
        trans_client = TransactionServiceClient(client)
        report: Report = await trans_client.get_report(report_request)

        assert report.request == report_request
        assert len(report.transactions) == len(
            expected[Keys.json]['transactions'],
        )


class TestCreateTransaction:
    """Тестирует метод create_transaction."""

    username = 'george'
    amount = 1
    timestamp = datetime(year=2024, month=1, day=1)  # noqa: WPS432 test value

    test_transaction = Transaction(
        username=username,
        amount=amount,
        timestamp=timestamp,
        transaction_type=TransactionType.deposit,
    )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'transaction, expected_status_code',
        (
            pytest.param(
                test_transaction,
                status.HTTP_201_CREATED,
                id='valid response 201',
            ),
            pytest.param(
                test_transaction,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                id='response 500',
                marks=pytest.mark.xfail(raises=HTTPException),
            ),
        ),
    )
    async def test_get_report(self, transaction, expected_status_code, client):
        """Тестирует ответ и тело ответа."""
        client = client(
            status_code=expected_status_code,
        )
        trans_client = TransactionServiceClient(client)
        response = await trans_client.create_transaction(transaction)

        assert response == good_response
