from urllib.parse import quote

import httpx

from dashboard.models import DiscUsage, ServiceStatus


class ApiUnavailableError(Exception): ...


class ApiClient:
    """Thin wrapper over the homelab API.

    Connection failures surface as ``ApiUnavailableError`` so the UI can show an
    offline state. A 404 for a single service or disc means it has no recorded
    data yet and is returned as ``None``; any other HTTP error is raised.
    """

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def _get(self, path: str) -> httpx.Response:
        try:
            return self._http.get(path)
        except httpx.TransportError as exc:
            raise ApiUnavailableError(str(exc)) from exc

    def _get_json(self, path: str) -> dict:
        response = self._get(path)
        response.raise_for_status()
        return response.json()

    def _get_optional_json(self, path: str) -> dict | None:
        response = self._get(path)
        if response.status_code == httpx.codes.NOT_FOUND:
            return None
        response.raise_for_status()
        return response.json()

    def service_count(self) -> int:
        return self._get_json("/service-count")["services"]

    def service_names(self) -> list[str]:
        return list(self._get_json("/services")["services"])

    def service(self, name: str) -> ServiceStatus | None:
        data = self._get_optional_json(f"/service/{quote(name, safe='')}")
        return ServiceStatus.model_validate(data) if data else None

    def disc_mounts(self) -> list[str]:
        return list(self._get_json("/discs")["discs"])

    def disc(self, mount: str) -> DiscUsage | None:
        data = self._get_optional_json(f"/disc/{quote(mount.lstrip('/'))}")
        return DiscUsage.model_validate(data) if data else None
