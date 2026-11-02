from pydantic import BaseModel


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
