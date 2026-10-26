import os
import socket
from abc import ABC, abstractmethod
from typing import Literal

import requests


class Service(ABC):
    def __init__(self, port: int, method: Literal["http", "tcp"]) -> None:
        super().__init__()
        self.port = port
        self.method = method

    @property
    def host(self) -> str:
        return "http://192.168.0.29:"

    def _http_is_up(self, **kwargs) -> bool:
        if kwargs:
            url = f"{self.host}{self.port}/{kwargs.get('health')}"
        else:
            url = f"{self.host}{self.port}"
        try:
            response = requests.get(url, timeout=5)
            return 200 <= response.status_code < 300
        except requests.RequestException:
            return False

    def _tcp_is_up(self) -> bool:
        host = self.host.replace("http://", "").replace(":", "")
        try:
            with socket.create_connection((host, self.port), timeout=3):
                return True
        except OSError:
            return False

    @abstractmethod
    def is_up(self, **kwargs) -> bool:
        match self.method:
            case "http":
                return self._http_is_up(**kwargs)
            case "tcp":
                return self._tcp_is_up()


class Chapflix(Service):
    def is_up(self, **kwargs) -> bool:
        return super().is_up()


class ChapflixAPI(Service):
    def is_up(self, **kwargs) -> bool:
        return super().is_up(health="health")


class PyPi(Service):
    def is_up(self, **kwargs) -> bool:
        return super().is_up()


class LogListener(Service):
    def is_up(self, **kwargs) -> bool:
        return super().is_up()


class RustFS(Service):
    def is_up(self, **kwargs) -> bool:
        return super().is_up(health="health")


class Kaneo(Service):
    def __init__(self, port: int, method: Literal["http", "tcp"]) -> None:
        super().__init__(port, method)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {os.getenv('KANEO_KEY')}",
                "Accept": "application/json",
            }
        )

    def is_up(self, **kwargs) -> bool:
        response = self.session.request("GET", f"{self.host}{self.port}/{kwargs.get('health')}")
        return 200 <= response.status_code < 300


class Postgres(Service):
    def is_up(self, **kwargs) -> bool:
        return super().is_up()


SERVICES = {
    "Chapflix": Chapflix(8042, "http"),
    "ChapflixAPI": ChapflixAPI(8043, "http"),
    "PyPi": PyPi(8080, "http"),
    "RustFS": RustFS(9001, "http"),
    "Kaneo": Kaneo(5173, "http"),
    "Postgres": Postgres(6543, "tcp"),
    "LogListener": LogListener(9020, "tcp"),
}

for service in SERVICES.values():
    print(service.is_up())
