import pytest
from dashboard.formatting import percent, size_from_gib
from dashboard.models import DiscUsage


def _disc(free: float, size: float = 100.0, warning: float = 0.25) -> DiscUsage:
    return DiscUsage(
        name="/dev/sda1",
        mount="/media/x",
        size=size,
        used=size - free,
        free=free,
        warning=warning,
    )


@pytest.mark.parametrize(
    ("free", "expected"),
    [(24.9, True), (25.0, False), (80.0, False)],
)
def test_disc_is_low_below_warning_fraction(free: float, expected: bool) -> None:
    assert _disc(free).is_low is expected


def test_zero_size_disc_does_not_divide_by_zero() -> None:
    assert _disc(free=0.0, size=0.0).free_fraction == 0.0


@pytest.mark.parametrize(
    ("fraction", "expected"),
    [(1.0, "100%"), (0.0, "0%"), (0.9951, "99.5%")],
)
def test_percent(fraction: float, expected: str) -> None:
    assert percent(fraction) == expected


@pytest.mark.parametrize(
    ("gib", "expected"),
    [(915.47, "915.5 GiB"), (2048.0, "2.00 TiB")],
)
def test_size_from_gib(gib: float, expected: str) -> None:
    assert size_from_gib(gib) == expected
