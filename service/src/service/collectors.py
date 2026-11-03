from service.availability import write_availability
from service.usage import write_discs


def main() -> None:
    write_availability()
    write_discs()


if __name__ == "__main__":
    main()
