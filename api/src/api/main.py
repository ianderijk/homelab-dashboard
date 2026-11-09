from fastapi import FastAPI

from api.models import Disc, Service
from api.service import (
    get_disc_data,
    get_service_data,
    get_number_services,
    get_service_names,
    get_disc_names,
    get_latest_temp_record
)

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
def get_services() -> dict:
    return get_service_names()


@app.get("/service-count")
def get_num_services() -> dict:
    return get_number_services()


@app.get("/discs")
def get_discs() -> dict:
    return get_disc_names()


@app.get("/latest-temp")
def get_latest_temp() -> dict:
    temp = get_latest_temp_record()
    return temp.model_dump()
