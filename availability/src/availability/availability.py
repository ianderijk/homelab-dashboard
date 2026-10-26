import os
import socket
from abc import ABC, abstractmethod

import requests


class Service(ABC):
    def __init__(self, port: int) -> None:
        super().__init__()
        self.port = port

    @property
    def host(self) -> str:
        return "http://192.168.0.29:"

    @abstractmethod
    def is_up(self, **kwargs) -> bool:
        if kwargs:
            url = f"{self.host}{self.port}/{kwargs.get('health')}"
        else:
            url = f"{self.host}{self.port}"
        try:
            response = requests.get(url, timeout=5)
            return 200 <= response.status_code < 300
        except requests.RequestException:
            return False


class Chapflix(Service):
    def is_up(self, **kwargs) -> bool:
        return super().is_up()


class ChapflixAPI(Service):
    def is_up(self, **kwargs) -> bool:
        return super().is_up(health="health")


class PyPi(Service):
    def is_up(self, **kwargs) -> bool:
        return super().is_up()


class RustFS(Service):
    def is_up(self, **kwargs) -> bool:
        return super().is_up(health="health")


class Kaneo(Service):
    def __init__(self, port: int) -> None:
        super().__init__(port)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {os.getenv('KANEO_KEY')}",
                "Accept": "application/json",
            }
        )

    def is_up(self, **kwargs) -> bool:
        response = self.session.request("GET", f"{self.host}{self.port}/health")
        return 200 <= response.status_code < 300


class Postgres(Service):
    def is_up(self, **kwargs) -> bool:
        host = self.host.replace("http://", "").replace(":", "")
        try:
            with socket.create_connection((host, self.port), timeout=3):
                return True
        except OSError as e:
            print(type(e).__name__, e)
            return False


SERVICES = {
    "Chapflix": Chapflix(8042),
    "ChapflixAPI": ChapflixAPI(8043),
    "PyPi": PyPi(8080),
    "RustFS": RustFS(9001),
    "Kaneo": Kaneo(5173),
    "Postgres": Postgres(6543),
}
