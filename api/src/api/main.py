from fastapi import FastAPI

from api.models import Disc, Service
from api.service import get_disc_data, get_service_data

app = FastAPI()


@app.get("/health")
def health() -> dict:
    return {"status": True}


@app.get("/service/{service_name}")
def get_service(service_name: str) -> Service:
    return get_service_data(service_name)


@app.get("/disc/{mount:path}")
def get_disc(mount: str) -> Disc:
    return get_disc_data(f"/{mount.lstrip('/')}")
