from dataclasses import dataclass
from datetime import datetime

from dashboard.client import ApiClient
from dashboard.models import DiscUsage, ServiceStatus, TemperatureReading


@dataclass(frozen=True)
class ServiceRow:
    name: str
    status: ServiceStatus | None


@dataclass(frozen=True)
class DiscRow:
    mount: str
    usage: DiscUsage | None


@dataclass(frozen=True)
class Overview:
    service_count: int
    services: list[ServiceRow]
    discs: list[DiscRow]
    temperature: TemperatureReading | None
    fetched_at: datetime

    @property
    def services_reporting(self) -> int:
        return sum(1 for row in self.services if row.status is not None)

    @property
    def services_up(self) -> int:
        return sum(1 for row in self.services if row.status and row.status.status)

    @property
    def discs_low(self) -> int:
        return sum(1 for row in self.discs if row.usage and row.usage.is_low)


def fetch_overview(api: ApiClient) -> Overview:
    return Overview(
        service_count=api.service_count(),
        services=[ServiceRow(name, api.service(name)) for name in api.service_names()],
        discs=[DiscRow(mount, api.disc(mount)) for mount in api.disc_mounts()],
        temperature=api.temperature(),
        fetched_at=datetime.now().astimezone(),
    )
