from unittest.mock import AsyncMock, MagicMock

import pytest


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
