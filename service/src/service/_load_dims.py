from utils.dbutils import execute_statement


def services() -> None:
    services = {
        "Chapflix": 8042,
        "ChapflixAPI": 8043,
        "PyPi": 8080,
        "RustFS": 9001,
        "Kaneo": 5173,
        "Postgres": 6543,
        "LogListener": 9020,
    }
    for k, v in services.items():
        insert = "insert into dim_services (service_name, port) values (:service_name, :port);"
        params = {"service_name": k, "port": v}
        execute_statement(insert, params)


def discs() -> None:
    discs = {
        "/dev/sdb1": "/media/ianderijk/ChapflixMed",
        "/dev/sda1": "/media/ianderijk/Backup",
    }
    for k, v in discs.items():
        insert = (
            "insert into dim_discs (mount, filesystem) values (:mount, :filesystem);"
        )
        params = {"mount": k, "filesystem": v}
        execute_statement(insert, params)


def main():
    services()
    discs()


if __name__ == "__main__":
    main()
