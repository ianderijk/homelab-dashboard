import httpx
import pytest
import respx
from dashboard.client import ApiClient, ApiUnavailableError


def test_lists_and_counts(api: ApiClient, healthy_api: respx.MockRouter) -> None:
    assert api.service_count() == 3
    assert api.service_names() == ["Chapflix", "Kaneo", "New"]
    assert api.disc_mounts() == ["/media/ok", "/media/full"]


def test_service_without_data_is_none(
    api: ApiClient, healthy_api: respx.MockRouter
) -> None:
    assert api.service("New") is None


def test_service_name_is_url_quoted(api: ApiClient, api_mock: respx.MockRouter) -> None:
    route = api_mock.get("/service/My%20App").respond(
        json={"name": "My App", "port": 1, "status": True, "uptime": 1.0}
    )

    status = api.service("My App")

    assert route.called
    assert status is not None
    assert status.name == "My App"


def test_disc_mount_maps_onto_path(
    api: ApiClient, healthy_api: respx.MockRouter
) -> None:
    disc = api.disc("/media/full")

    assert disc is not None
    assert disc.name == "/dev/sdb1"


def test_temperature(api: ApiClient, healthy_api: respx.MockRouter) -> None:
    reading = api.temperature()

    assert reading is not None
    assert reading.temp == 65.0
    assert reading.critical == 70.0


def test_temperature_without_data_is_none(
    api: ApiClient, api_mock: respx.MockRouter
) -> None:
    api_mock.get("/latest-temp").respond(404, json={"detail": "No data"})

    assert api.temperature() is None


def test_connection_failure_raises_unavailable(
    api: ApiClient, api_mock: respx.MockRouter
) -> None:
    api_mock.get("/service-count").mock(side_effect=httpx.ConnectError("refused"))

    with pytest.raises(ApiUnavailableError):
        api.service_count()


def test_server_error_is_not_swallowed(
    api: ApiClient, api_mock: respx.MockRouter
) -> None:
    api_mock.get("/service/Chapflix").respond(500)

    with pytest.raises(httpx.HTTPStatusError):
        api.service("Chapflix")
