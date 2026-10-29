import sqlite3
from pathlib import Path


def _get_db_path() -> Path:
    root = Path(__file__).parents
    return root[3] / "dashboard.db"


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
