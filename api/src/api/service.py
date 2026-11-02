from typing import Any

from fastapi import HTTPException
from utils.dbutils import execute_query

from api.models import Disc, Service


def _get_service_details(service_name: str) -> dict[str, Any]:
    query = """
    select ds.service_id
        ,ds.service_name
        ,ds.port
        ,fs.status
        ,fs.datetime
    from fact_services as fs
    inner join dim_services as ds on fs.service_id = ds.service_id
    where ds.service_name = :service_name
    order by fs.datetime desc
    limit 1
    """
    params = {"service_name": service_name}
    data = execute_query(query, params)
    if not data:
        raise HTTPException(
            status_code=404, detail=f"No data for service {service_name}"
        )
    values = (
        "service_id",
        "service_name",
        "port",
        "status",
        "datetime",
    )
    return {k: v for k, v in zip(values, data[0])}


def _calculate_service_uptime(service_name: str) -> float:
    query = """
    select avg(fs.status)
    from fact_services as fs
    inner join dim_services as ds on fs.service_id = ds.service_id
    where ds.service_name = :service_name;
    """
    params = {"service_name": service_name}
    data = execute_query(query, params)
    return data[0][0] or 0.0


def get_service_data(service_name: str) -> Service:
    service_details = _get_service_details(service_name)
    uptime = _calculate_service_uptime(service_name)
    service = Service(
        name=service_details["service_name"],
        port=service_details["port"],
        status=service_details["status"],
        uptime=uptime,
    )
    return service


def _convert_kib_to_gib(value: int) -> float:
    return value / 1024**2


def get_disc_data(mount: str) -> Disc:
    query = """
    select dd.mount
        ,dd.filesystem
        ,fd.space
        ,fd.used
    from fact_discs as fd
    inner join dim_discs as dd on fd.disc_id = dd.disc_id
    where dd.mount = :mount
    order by fd.id desc
    limit 1;
    """
    params = {"mount": mount}
    data = execute_query(query, params)
    if not data:
        raise HTTPException(status_code=404, detail=f"No data for disc {mount}")
    mount, filesystem, space, used = data[0]

    return Disc(
        name=filesystem,
        mount=mount,
        size=_convert_kib_to_gib(space),
        used=_convert_kib_to_gib(used),
        free=_convert_kib_to_gib(space - used),
    )


def get_number_services() -> dict[str, int]:
    query = "select count(service_id) from dim_services;"
    data = execute_query(query)
    return {"services": data[0][0]}
