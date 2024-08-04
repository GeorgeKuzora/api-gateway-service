import pytest
from fastapi import status


class TestIsUp:
    """Тестирует хэндлер healthz/up."""

    url = 'healthz/up'

    @pytest.mark.asyncio
    @pytest.mark.anyio
    async def test_good_response(self, test_client):
        """Тестирует успешный ответ."""
        response = await test_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK


class TestIsReady:
    """Тестирует хэндлер healthz/ready."""

    url = 'healthz/ready'

    @pytest.mark.asyncio
    @pytest.mark.anyio
    @pytest.mark.parametrize(
        'expected_response_status_code',
        (
            pytest.param(
                status.HTTP_200_OK,
                id='valid - response status 200',
            ),
            pytest.param(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                id='service response status code 503',
            ),
        ),
    )
    async def test_auth_service_response_status_code(
        self,
        expected_response_status_code,
        test_client,
        auth_client_healthz_mocker,
        transaction_client_healthz_mocker,
    ):
        """Тестирует коды ответов хэндлера healthz/ready."""
        auth_client_healthz_mocker(
            status_code=expected_response_status_code,
        )
        transaction_client_healthz_mocker(
            status_code=status.HTTP_200_OK,
        )
        response = await test_client.get(self.url)

        assert response.status_code == expected_response_status_code

    @pytest.mark.asyncio
    @pytest.mark.anyio
    @pytest.mark.parametrize(
        'expected_response_status_code',
        (
            pytest.param(
                status.HTTP_200_OK,
                id='valid - response status 200',
            ),
            pytest.param(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                id='service response status code 503',
            ),
        ),
    )
    async def test_transaction_service_response_status_code(
        self,
        expected_response_status_code,
        test_client,
        auth_client_healthz_mocker,
        transaction_client_healthz_mocker,
    ):
        """Тестирует коды ответов хэндлера healthz/ready."""
        auth_client_healthz_mocker(
            status_code=status.HTTP_200_OK,
        )
        transaction_client_healthz_mocker(
            status_code=expected_response_status_code,
        )
        response = await test_client.get(self.url)

        assert response.status_code == expected_response_status_code
