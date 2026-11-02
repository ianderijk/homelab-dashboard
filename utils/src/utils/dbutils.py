import sqlite3
from pathlib import Path

from utils.constants import ROOT


def _get_db_path() -> Path:
    return ROOT / "ExtDrive/homelab-dashboard/dashboard.db"


DB_PATH = _get_db_path()


def execute_statement(statement: str, params: dict | None = None) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(statement, params or {})


def execute_query(query: str, params: dict | None = None) -> list:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        results = cursor.execute(query, params or {}).fetchall()
        return results
