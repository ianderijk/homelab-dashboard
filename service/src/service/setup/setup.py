from service.setup.tables import create_tables
from service.setup.load_dims import create_dims


def main() -> None:
    create_tables()
    create_dims()


if __name__ == "__main__":
    main()
