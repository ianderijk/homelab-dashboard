from pydantic import BaseModel


class Service(BaseModel):
    name: str
    port: int
    status: bool
    uptime: float


class Disc(BaseModel):
    name: str
    mount: str
    size: float
    used: float
    free: float
    warning: float = 0.25


class Temperature(BaseModel):
    temp: float
    warning: float = 60
    critical: float = 70
