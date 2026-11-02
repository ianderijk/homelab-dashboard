import uvicorn

from dashboard.config import load_settings


def main() -> None:
    settings = load_settings()
    uvicorn.run("dashboard.app:app", host=settings.host, port=settings.port)
