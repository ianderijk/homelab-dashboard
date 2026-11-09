import subprocess
from datetime import UTC, datetime

from utils.dbutils import execute_statement

class Temperature:
    def __init__(self, temp: float) -> None:
        self.temp = temp

    @property
    def record_timestamp(self) -> datetime:
        return datetime.now(tz=UTC)


def get_temp() -> Temperature:
    result = subprocess.run(
        ["vcgencmd", "measure_temp"], capture_output=True, check=True, text=True
    )
    if result.returncode == 0:
        measure = result.stdout
        temp = float(measure[measure.index("=") + 1 :-3])
        return Temperature(temp)

    return Temperature(0.0)


def write_temp_record() -> None:
    temp = get_temp()
    insert = "insert into fact_temp (temp, datetime) values (:temp, :datetime)"
    params = {"temp": temp.temp, "datetime": temp.record_timestamp}
    execute_statement(insert, params)
