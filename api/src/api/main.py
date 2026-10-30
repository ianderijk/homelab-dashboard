from fastapi import FastAPI

from api.service import get_service_data

app = FastAPI()

@app.get("service/{service-name}")
def get_service(service_name: str) -> dict:
    service = get_service_data(service_name)
    return service.model_dump()
