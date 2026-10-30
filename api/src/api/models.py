from pydantic import BaseModel


class Service(BaseModel):
    name: str
    port: int
    status: bool
    uptime: float


class Disc(BaseModel):
    name: str
    mount: str
    size: int
    used: int