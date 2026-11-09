from service.availability import write_availability
from service.usage import write_discs
from service.temperature import write_temp_record


def main() -> None:
    write_availability()
    write_discs()
    write_temp_record()


if __name__ == "__main__":
    main()
