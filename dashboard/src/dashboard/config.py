import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    api_url: str
    host: str
    port: int
    refresh_seconds: int
    api_timeout_seconds: float


def load_settings() -> Settings:
    return Settings(
        api_url=os.getenv("DASHBOARD_API_URL", "http://127.0.0.1:8000"),
        host=os.getenv("DASHBOARD_HOST", "192.168.0.29"),
        port=int(os.getenv("DASHBOARD_PORT", "8001")),
        refresh_seconds=int(os.getenv("DASHBOARD_REFRESH_SECONDS", "60")),
        api_timeout_seconds=float(os.getenv("DASHBOARD_API_TIMEOUT_SECONDS", "5")),
    )
