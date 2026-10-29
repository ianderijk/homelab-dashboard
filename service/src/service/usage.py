import subprocess

from utils.dbutils import execute_query, execute_statement
from utils.constants import ROOT


class Drive:
    def __init__(
        self,
        mount: str,
        filesystem: str,
        space: int,
        used: int,
        available: int,
        free: str,
    ) -> None:
        self.mount = mount
        self.filesystem = filesystem
        self.space = space
        self.used = used
        self.available = available
        self.free = free

    def __str__(self) -> str:
        return f"{self.mount}: {self.free}"

    @property
    def disc_id(self) -> int:
        query = "select disc_id from dim_discs where mount = :mount;"
        params = {"mount": self.mount}
        data = execute_query(query, params)
        return data[0][0]


def find_drives() -> list[Drive]:
    result = subprocess.run(["df"], check=True, stdout=subprocess.PIPE).stdout
    data = str(result).split("\\n")
    drives = []
    for entry in data:
        if str(ROOT) not in entry:
            continue
        line = [x for x in entry.split() if x != ""]
        mount = line[-1]
        filesystem = line[0]
        space = int(line[1])
        used = int(line[2])
        available = int(line[3])
        free = line[4]
        drive = Drive(
            mount=mount,
            filesystem=filesystem,
            space=space,
            used=used,
            available=available,
            free=free,
        )
        drives.append(drive)
    return drives


def record_drives(drives: list[Drive]) -> None:
    for drive in drives:
        insert = "insert into fact_discs (disc_id, space, used, free) values (:disc_id, :space, :used, :free);"
        params = {"disc_id": drive.disc_id, "space": drive.space, "used": drive.used, "free": drive.free}
        execute_statement(insert, params)


def main() -> None:
    drives = find_drives()
    record_drives(drives)


if __name__ == "__main__":
    main()
