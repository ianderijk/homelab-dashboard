from collections.abc import Iterator

import httpx
import pytest
import respx
from dashboard.client import ApiClient

API_URL = "http://api.test"


@pytest.fixture
def api_mock() -> Iterator[respx.MockRouter]:
    with respx.mock(base_url=API_URL, assert_all_called=False) as router:
        yield router


@pytest.fixture
def api(api_mock: respx.MockRouter) -> Iterator[ApiClient]:
    with httpx.Client(base_url=API_URL) as http:
        yield ApiClient(http)


@pytest.fixture
def healthy_api(api_mock: respx.MockRouter) -> respx.MockRouter:
    router = api_mock
    router.get("/service-count").respond(json={"services": 3})
    router.get("/services").respond(json={"services": ["Chapflix", "Kaneo", "New"]})
    router.get("/service/Chapflix").respond(
        json={"name": "Chapflix", "port": 8042, "status": True, "uptime": 0.995}
    )
    router.get("/service/Kaneo").respond(
        json={"name": "Kaneo", "port": 5173, "status": False, "uptime": 0.5}
    )
    router.get("/service/New").respond(404, json={"detail": "No data"})
    router.get("/discs").respond(json={"discs": ["/media/ok", "/media/full"]})
    router.get("/disc/media/ok").respond(
        json={
            "name": "/dev/sda1",
            "mount": "/media/ok",
            "size": 1000.0,
            "used": 400.0,
            "free": 600.0,
            "warning": 0.25,
        }
    )
    router.get("/disc/media/full").respond(
        json={
            "name": "/dev/sdb1",
            "mount": "/media/full",
            "size": 1000.0,
            "used": 900.0,
            "free": 100.0,
            "warning": 0.25,
        }
    )
    router.get("/latest-temp").respond(
        json={"temp": 65.0, "warning": 60.0, "critical": 70.0}
    )
    return router
