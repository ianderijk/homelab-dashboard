from typing import Literal

from pydantic import BaseModel

Level = Literal["good", "warning", "critical"]


class ServiceStatus(BaseModel):
    name: str
    port: int
    status: bool
    uptime: float


class DiscUsage(BaseModel):
    name: str
    mount: str
    size: float
    used: float
    free: float
    warning: float

    @property
    def free_fraction(self) -> float:
        return self.free / self.size if self.size else 0.0

    @property
    def used_fraction(self) -> float:
        return self.used / self.size if self.size else 0.0

    @property
    def is_low(self) -> bool:
        return self.free_fraction < self.warning


class TemperatureReading(BaseModel):
    temp: float
    warning: float
    critical: float

    @property
    def level(self) -> Level:
        if self.temp > self.critical:
            return "critical"
        if self.temp >= self.warning:
            return "warning"
        return "good"
