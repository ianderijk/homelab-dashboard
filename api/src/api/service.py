from typing import Any

from api.models import Service, Disc
from utils.dbutils import execute_query


def _get_service_details(service_name: str) -> dict[str, Any]:
    query = """
    select ds.service_id
        ,ds.service_name
        ,ds.port
        ,fs.status
        ,fs.datetime
    from fact_services as fs
    left join dim_services as ds on fs.service_id = ds.service_id
    where ds.service_name = :service_name
    limit 1
    """
    params = {"service_name": service_name}
    data = execute_query(query, params)
    values = (
        "service_id",
        "service_name",
        "port",
        "status",
        "datetime"
    )
    return {k: v for k, v in zip(values, data[0])}


def _calculate_service_uptime(service_name: str) -> float:
    query = """
    select fs.status
        ,fs.datetime
    from fact_services as fs
    left join dim_services as ds on fs.service_id = ds.service_id
    where ds.service_name = :service_name
    """
    params = {"service_name": service_name}
    data = execute_query(query, params)

    uptime = 0
    downtime = 0
    for i, record in enumerate(data):
        if i == len(data) - 1:
            break

        cur_status = record[0]
        next_status = data[i][0]
        if cur_status and next_status:
            uptime += 1
        elif not next_status:
            downtime += 1

    return uptime / (uptime + downtime)


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
