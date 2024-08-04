from datetime import datetime
from enum import StrEnum

import pytest
from fastapi import status


class Key(StrEnum):
    """Часто повторяемые ключи."""

    encoded_token = 'encoded_token'  # noqa: S105 key
    authorization = 'Authorization'
    transactions = 'transactions'
    http_protocol_prefix = 'http://'
    https_protocol_prefix = 'https://'
    username = 'username'
    password = 'password'  # noqa: S105 test key
    invalid = 'invalid'
    token = 'token'  # noqa: S105 test key
    body = 'body'
    headers = 'headers'
    start_date = 'start_date'
    end_date = 'end_date'
    request = 'request'
    amount = 'amount'
    transaction_type = 'transaction_type'
    timestamp = 'timestamp'


valid_request_body = {Key.username: 'george', Key.password: 'password123'}
invalid_request_body = {Key.invalid: 'peter', Key.invalid: 'passw'}
valid_request_headers = {Key.authorization: 'Bearer fasdfqwr.wer32fsd.3tadf'}
invalid_request_headers = {Key.invalid: 'Bearer invalid'}
stub_resp_body = {Key.encoded_token: 'encoded_tock'}
expected_response = {Key.token: stub_resp_body[Key.encoded_token]}
transaction_date = datetime(year=2024, month=1, day=15).isoformat()  # noqa: WPS432, E501 test value
start_date = datetime(year=2024, month=1, day=1).isoformat()  # noqa: WPS432, E501 test value
end_date = datetime(year=2024, month=1, day=30).isoformat()  # noqa: WPS432, E501 test value


class TestRegister:
    """Тестирует хэндлер auth/register."""

    url = 'auth/register'

    @pytest.mark.asyncio
    @pytest.mark.anyio
    async def test_register_good_response(
        self, test_client, auth_client_mocker,
    ):
        """Тестирует метод register успешный ответ."""
        auth_client_mocker(
            status_code=status.HTTP_200_OK,
            json=stub_resp_body,
        )
        response = await test_client.post(self.url, json=valid_request_body)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    @pytest.mark.asyncio
    @pytest.mark.anyio
    @pytest.mark.parametrize(
        'request_body, expected_response_status_code',
        (
            pytest.param(
                valid_request_body,
                status.HTTP_200_OK,
                id='valid - response status 200',
            ),
            pytest.param(
                invalid_request_body,
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                id='invalid request body - response status 422',
            ),
            pytest.param(
                valid_request_body,
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                id='service response status code 422',
            ),
            pytest.param(
                valid_request_body,
                status.HTTP_404_NOT_FOUND,
                id='service response status code 404',
            ),
            pytest.param(
                valid_request_body,
                status.HTTP_401_UNAUTHORIZED,
                id='service response status code 401',
            ),
            pytest.param(
                valid_request_body,
                status.HTTP_503_SERVICE_UNAVAILABLE,
                id='service response status code 503',
            ),
        ),
    )
    async def test_response_status_code(
        self,
        request_body,
        expected_response_status_code,
        test_client,
        auth_client_mocker,
    ):
        """Тестирует коды ответов хэндлера auth/register."""
        auth_client_mocker(
            status_code=expected_response_status_code,
            json=stub_resp_body,
        )
        response = await test_client.post(self.url, json=request_body)

        assert response.status_code == expected_response_status_code


class TestLogin:
    """Тестирует хэндлер auth/login."""

    url = 'auth/login'

    @pytest.mark.asyncio
    @pytest.mark.anyio
    async def test_good_response(
        self, test_client, auth_client_mocker,
    ):
        """Тестирует успешный ответ."""
        auth_client_mocker(
            status_code=status.HTTP_200_OK,
            json=stub_resp_body,
        )
        response = await test_client.post(
            self.url, json=valid_request_body, headers=valid_request_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    @pytest.mark.asyncio
    @pytest.mark.anyio
    @pytest.mark.parametrize(
        'request_data, expected_response_status_code',
        (
            pytest.param(
                {
                    Key.body: valid_request_body,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_200_OK,
                id='valid - response status 200',
            ),
            pytest.param(
                {
                    Key.body: invalid_request_body,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                id='invalid request body - response status 422',
            ),
            pytest.param(
                {
                    Key.body: valid_request_body,
                    Key.headers: invalid_request_headers,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                id='invalid request headers - response status 422',
            ),
            pytest.param(
                {
                    Key.body: valid_request_body,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                id='service response status code 422',
            ),
            pytest.param(
                {
                    Key.body: valid_request_body,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_404_NOT_FOUND,
                id='service response status code 404',
            ),
            pytest.param(
                {
                    Key.body: valid_request_body,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_401_UNAUTHORIZED,
                id='service response status code 401',
            ),
            pytest.param(
                {
                    Key.body: valid_request_body,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_503_SERVICE_UNAVAILABLE,
                id='service response status code 503',
            ),
        ),
    )
    async def test_response_status_code(
        self,
        request_data,
        expected_response_status_code,
        test_client,
        auth_client_mocker,
    ):
        """Тестирует коды ответов хэндлера auth/login."""
        auth_client_mocker(
            status_code=expected_response_status_code,
            json=stub_resp_body,
        )
        response = await test_client.post(
            self.url,
            json=request_data[Key.body],
            headers=request_data[Key.headers],
        )

        assert response.status_code == expected_response_status_code


class TestGetReport:
    """Тестирует хэндлер transaction/report."""

    valid_report_request = {
        str(Key.username): 'max',
        str(Key.start_date): start_date,
        str(Key.end_date): end_date,
    }
    invalid_report_request = {
        str(Key.invalid): 'invalid',
        str(Key.start_date): start_date,
        str(Key.end_date): end_date,
    }
    stub_transaction = {
        str(Key.username): 'max',
        str(Key.amount): 1,
        str(Key.transaction_type): 0,
        str(Key.timestamp): transaction_date,
    }
    stub_report_response = {
        str(Key.request): valid_report_request,
        str(Key.transactions): [stub_transaction, stub_transaction],
    }
    url = 'transaction/report'

    @pytest.mark.asyncio
    @pytest.mark.anyio
    @pytest.mark.parametrize(
        'request_data, expected_response_status_code',
        (
            pytest.param(
                {
                    Key.body: valid_report_request,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_200_OK,
                id='valid - response status 200',
            ),
            pytest.param(
                {
                    Key.body: valid_report_request,
                    Key.headers: invalid_request_headers,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                id='invalid request headers - response status 422',
            ),
            pytest.param(
                {
                    Key.body: valid_report_request,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                id='service response status code 422',
            ),
            pytest.param(
                {
                    Key.body: valid_report_request,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_404_NOT_FOUND,
                id='service response status code 404',
            ),
            pytest.param(
                {
                    Key.body: valid_report_request,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_401_UNAUTHORIZED,
                id='service response status code 401',
            ),
            pytest.param(
                {
                    Key.body: valid_report_request,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_503_SERVICE_UNAVAILABLE,
                id='service response status code 503',
            ),
        ),
    )
    async def test_response_status_code_from_check_token(
        self,
        request_data,
        expected_response_status_code,
        test_client,
        auth_client_mocker,
        transaction_client_mocker,
    ):
        """Тестирует коды ответов хэндлера auth/login."""
        auth_client_mocker(
            status_code=expected_response_status_code,
        )
        transaction_client_mocker(
            status_code=status.HTTP_200_OK,
            json=self.stub_report_response,
        )
        response = await test_client.post(
            self.url,
            json=request_data[Key.body],
            headers=request_data[Key.headers],
        )

        assert response.status_code == expected_response_status_code

    @pytest.mark.asyncio
    @pytest.mark.anyio
    @pytest.mark.parametrize(
        'request_data, expected_response_status_code',
        (
            pytest.param(
                {
                    Key.body: valid_report_request,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_200_OK,
                id='valid - response status 200',
            ),
            pytest.param(
                {
                    Key.body: invalid_report_request,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                id='invalid request body - response status 422',
            ),
            pytest.param(
                {
                    Key.body: valid_report_request,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                id='service response status code 422',
            ),
            pytest.param(
                {
                    Key.body: valid_report_request,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_404_NOT_FOUND,
                id='service response status code 404',
            ),
            pytest.param(
                {
                    Key.body: valid_report_request,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_401_UNAUTHORIZED,
                id='service response status code 401',
            ),
            pytest.param(
                {
                    Key.body: valid_report_request,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_503_SERVICE_UNAVAILABLE,
                id='service response status code 503',
            ),
        ),
    )
    async def test_response_status_code_from_get_report(
        self,
        request_data,
        expected_response_status_code,
        test_client,
        auth_client_mocker,
        transaction_client_mocker,
    ):
        """Тестирует коды ответов хэндлера auth/login."""
        auth_client_mocker(
            status_code=status.HTTP_200_OK,
        )
        transaction_client_mocker(
            status_code=expected_response_status_code,
            json=self.stub_report_response,
        )
        response = await test_client.post(
            self.url,
            json=request_data[Key.body],
            headers=request_data[Key.headers],
        )

        assert response.status_code == expected_response_status_code

    @pytest.mark.asyncio
    @pytest.mark.anyio
    async def test_good_response(
        self, test_client, auth_client_mocker, transaction_client_mocker,
    ):
        """Тестирует успешный ответ."""
        auth_client_mocker(
            status_code=status.HTTP_200_OK,
        )
        transaction_client_mocker(
            status_code=status.HTTP_200_OK,
            json=self.stub_report_response,
        )
        response = await test_client.post(
            self.url,
            json=self.valid_report_request,
            headers=valid_request_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        assert (
            len(response.json()[Key.transactions]) ==
            len(self.stub_report_response[Key.transactions])
        )


class TestCreateTransaction:
    """Тестирует хэндлер transaction/transaction."""

    valid_transaction = {
        str(Key.username): 'charly',
        str(Key.amount): 1,
        str(Key.transaction_type): 0,
        str(Key.timestamp): transaction_date,
    }
    invalid_transaction = {
        str(Key.invalid): 'mike',
        str(Key.amount): 1,
        str(Key.transaction_type): 0,
        str(Key.timestamp): transaction_date,
    }
    url = 'transaction/transaction'

    @pytest.mark.asyncio
    @pytest.mark.anyio
    @pytest.mark.parametrize(
        'request_data, expected_response_status_code',
        (
            pytest.param(
                {
                    Key.body: valid_transaction,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_201_CREATED,
                id='valid - response status 200',
            ),
            pytest.param(
                {
                    Key.body: valid_transaction,
                    Key.headers: invalid_request_headers,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                id='invalid request headers - response status 422',
            ),
            pytest.param(
                {
                    Key.body: valid_transaction,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                id='service response status code 422',
            ),
            pytest.param(
                {
                    Key.body: valid_transaction,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_404_NOT_FOUND,
                id='service response status code 404',
            ),
            pytest.param(
                {
                    Key.body: valid_transaction,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_401_UNAUTHORIZED,
                id='service response status code 401',
            ),
            pytest.param(
                {
                    Key.body: valid_transaction,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_503_SERVICE_UNAVAILABLE,
                id='service response status code 503',
            ),
        ),
    )
    async def test_response_status_code_from_check_token(
        self,
        request_data,
        expected_response_status_code,
        test_client,
        auth_client_mocker,
        transaction_client_mocker,
    ):
        """Тестирует коды ответов хэндлера auth/login."""
        auth_client_mocker(
            status_code=expected_response_status_code,
        )
        transaction_client_mocker(
            status_code=status.HTTP_200_OK,
            json=self.valid_transaction,
        )
        response = await test_client.post(
            self.url,
            json=request_data[Key.body],
            headers=request_data[Key.headers],
        )

        assert response.status_code == expected_response_status_code

    @pytest.mark.asyncio
    @pytest.mark.anyio
    @pytest.mark.parametrize(
        'request_data, expected_response_status_code',
        (
            pytest.param(
                {
                    Key.body: valid_transaction,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_201_CREATED,
                id='valid - response status 201',
            ),
            pytest.param(
                {
                    Key.body: invalid_transaction,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                id='invalid request body - response status 422',
            ),
            pytest.param(
                {
                    Key.body: valid_transaction,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                id='service response status code 422',
            ),
            pytest.param(
                {
                    Key.body: valid_transaction,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_404_NOT_FOUND,
                id='service response status code 404',
            ),
            pytest.param(
                {
                    Key.body: valid_transaction,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_401_UNAUTHORIZED,
                id='service response status code 401',
            ),
            pytest.param(
                {
                    Key.body: valid_transaction,
                    Key.headers: valid_request_headers,
                },
                status.HTTP_503_SERVICE_UNAVAILABLE,
                id='service response status code 503',
            ),
        ),
    )
    async def test_response_status_code_from_get_report(
        self,
        request_data,
        expected_response_status_code,
        test_client,
        auth_client_mocker,
        transaction_client_mocker,
    ):
        """Тестирует коды ответов хэндлера auth/login."""
        auth_client_mocker(
            status_code=status.HTTP_200_OK,
        )
        transaction_client_mocker(
            status_code=expected_response_status_code,
            json=self.valid_transaction,
        )
        response = await test_client.post(
            self.url,
            json=request_data[Key.body],
            headers=request_data[Key.headers],
        )

        assert response.status_code == expected_response_status_code
