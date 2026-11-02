import httpx
import pytest
import respx
from dashboard.app import create_app, get_api
from dashboard.client import ApiClient
from dashboard.config import Settings

SETTINGS = Settings(
    api_url="http://api.test",
    host="127.0.0.1",
    port=0,
    refresh_seconds=30,
    api_timeout_seconds=1,
)

pytestmark = pytest.mark.anyio


async def _get(api: ApiClient, path: str) -> httpx.Response:
    app = create_app(SETTINGS)
    app.dependency_overrides[get_api] = lambda: api
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://dashboard.test"
    ) as client:
        return await client.get(path)


async def test_index_renders_overview(
    api: ApiClient, healthy_api: respx.MockRouter
) -> None:
    response = await _get(api, "/")

    assert response.status_code == 200
    html = response.text
    assert "<!DOCTYPE html>" in html
    assert 'hx-trigger="every 30s"' in html
    assert "Chapflix" in html
    assert "No data yet" in html
    assert "Low space" in html


async def test_panel_is_a_fragment(
    api: ApiClient, healthy_api: respx.MockRouter
) -> None:
    response = await _get(api, "/panels/overview")

    assert response.status_code == 200
    assert "<!DOCTYPE html>" not in response.text
    assert 'id="overview"' in response.text


async def test_offline_api_renders_notice(
    api: ApiClient, api_mock: respx.MockRouter
) -> None:
    api_mock.route().mock(side_effect=httpx.ConnectError("refused"))

    response = await _get(api, "/panels/overview")

    assert response.status_code == 200
    assert "API offline" in response.text
    assert 'hx-get="/panels/overview"' in response.text
