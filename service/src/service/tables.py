from service.dbutils import execute_statement

DIM_SERVICES = """
    create table if not exists  dim_services (
    service_id integer primary key autoincrement,
    service_name text,
    port integer
    );
    """

FACT_SERVICES = """
    create table if not exists fact_services (
    id integer primary key autoincrement,
    service_id integer,
    status bit,
    datetime timestamp
    )
    """

DIM_DISCS = """
    create table if not exists dim_discs (
    disc_id integer primary key autoincrement,
    mount text,
    filesystem text
    )
    """

FACT_DISCS = """
    create table if not exists fact_discs (
    id integer primary key autoincrement,
    disc_id integer,
    space integer,
    used integer,
    free numeric,
    datetime timestamp
    )
    """


def create_tables() -> None:
    execute_statement(DIM_SERVICES)
    execute_statement(FACT_SERVICES)
    execute_statement(DIM_DISCS)
    execute_statement(FACT_DISCS)


def drop_tables() -> None:
    tables = (
        "dim_services",
        "fact_services",
        "dim_discs",
        "fact_discs",
    )
    for table in tables:
        drop = f"drop table if exists {table};"
        execute_statement(drop)


if __name__ == "__main__":
    drop_tables()
    create_tables()
