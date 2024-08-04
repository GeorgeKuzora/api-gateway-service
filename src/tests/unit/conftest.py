from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient

from app.service import app


@pytest.fixture
def client():
    """Фикстура клиентa Client."""
    def _client(*, status_code, json=None, headers=None):  # noqa: WPS430, E501 for tests
        client = AsyncMock()
        response = MagicMock()
        response.status_code = status_code
        response.json.return_value = json
        response.headers = headers
        client.post.return_value = response
        return client
    return _client


@pytest.fixture(scope='session')
def test_client():
    """Создает тестовый клиент."""
    return AsyncClient(app=app, base_url='http://test')


@pytest.fixture
def auth_client_mocker(monkeypatch):
    """Фикстура мока метода post auth http клиента."""
    def _client(*, status_code, json=None, headers=None):  # noqa: WPS430, E501 for tests
        client = AsyncMock()
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = json
        mock_resp.headers = headers
        client.post.return_value = mock_resp
        monkeypatch.setattr(
            'app.api.handlers.clients.auth_client.client',
            client,
        )
    return _client


@pytest.fixture
def transaction_client_mocker(monkeypatch):
    """Фикстура мока метода post transaction http клиента."""
    def _client(*, status_code, json=None, headers=None):  # noqa: WPS430, E501 for tests
        client = AsyncMock()
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = json
        mock_resp.headers = headers
        client.get.return_value = mock_resp
        monkeypatch.setattr(
            'app.api.handlers.clients.transactions_client.client',
            client,
        )
    return _client


@pytest.fixture
def auth_client_healthz_mocker(monkeypatch):
    """Фикстура мока метода get auth http клиента."""
    def _client(*, status_code):  # noqa: WPS430, E501 for tests
        client = AsyncMock()
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        client.get.return_value = mock_resp
        monkeypatch.setattr(
            'app.api.healthz.handlers.clients.auth_client.client',
            client,
        )
    return _client


@pytest.fixture
def transaction_client_healthz_mocker(monkeypatch):
    """Фикстура мока метода get transaction http клиента."""
    def _client(*, status_code):  # noqa: WPS430, E501 for tests
        client = AsyncMock()
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        client.get.return_value = mock_resp
        monkeypatch.setattr(
            'app.api.healthz.handlers.clients.transactions_client.client',
            client,
        )
    return _client
