from fastapi import FastAPI

from api.models import Disc, Service
from api.service import get_disc_data, get_service_data, get_number_services

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


@app.get("/services")
def get_num_services() -> dict:
    return get_number_services()
