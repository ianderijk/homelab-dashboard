import os
from pathlib import Path


class MissingEnvVarError(Exception): ...


def _get_root() -> Path:
    root = os.getenv("ROOT")
    if root:
        return Path(root)

    raise MissingEnvVarError("No ROOT variable set.")

ROOT = _get_root()
