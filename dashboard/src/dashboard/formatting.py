def percent(fraction: float) -> str:
    return f"{fraction:.0%}" if fraction in (0, 1) else f"{fraction:.1%}"


def size_from_gib(gib: float) -> str:
    if gib >= 1024:
        return f"{gib / 1024:.2f} TiB"
    return f"{gib:.1f} GiB"


def celsius(value: float) -> str:
    return f"{value:.1f} °C"
