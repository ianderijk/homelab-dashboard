import os
import socket
from abc import ABC, abstractmethod
from typing import Literal
from datetime import UTC, datetime

import requests

from utils.dbutils import execute_query, execute_statement


class Service(ABC):
    def __init__(self, port: int, method: Literal["http", "tcp"], name: str) -> None:
        super().__init__()
        self.port = port
        self.method = method
        self.name = name

        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {os.getenv('KANEO_KEY', None)}",
                "Accept": "application/json",
            }
        )

    @property
    def host(self) -> str:
        return "http://192.168.0.29:"

    @property
    def service_id(self) -> int:
        query = (
            "select service_id from dim_services where service_name = :service_name;"
        )
        params = {"service_name": self.name}
        data = execute_query(query, params)
        return data[0][0]

    @property
    def record_datetime(self) -> datetime:
        return datetime.now(tz=UTC)

    def _http_is_up(self, **kwargs) -> bool:
        if kwargs:
            url = f"{self.host}{self.port}/{kwargs.get('health')}"
        else:
            url = f"{self.host}{self.port}"

        try:
            response = self._session.request("GET", url)
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
p    def is_up(self, **kwargs) -> bool:
        return super().is_up()


class RustFS(Service):
    def is_up(self, **kwargs) -> bool:
        return super().is_up(health="health")


class Kaneo(Service):
    def is_up(self, **kwargs) -> bool:
        return super().is_up(health="health")


class Postgres(Service):
    def is_up(self, **kwargs) -> bool:
        return super().is_up()


SERVICES = (
    Chapflix(8042, "http", "Chapflix"),
    ChapflixAPI(8043, "http", "ChapflixAPI"),
    PyPi(8080, "http", "PyPi"),
    RustFS(9001, "http", "RustFS"),
    Kaneo(5173, "http", "Kaneo"),
    Postgres(6543, "tcp", "Postgres"),
    LogListener(9020, "tcp", "LogListener"),
)


def write_availability() -> None:
    for service in SERVICES:
        insert = "insert into fact_services (service_id, status, datetime) values (:service_id, :status, :datetime);"
        params = {
            "service_id": service.service_id,
            "status": service.is_up(health="health"),
            "datetime": service.record_datetime,
        }
        execute_statement(insert, params)


if __name__ == "__main__":
    write_availability()
