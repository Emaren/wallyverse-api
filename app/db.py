from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .config import settings


def _db_path() -> Path:
    return Path(settings.db_path).resolve()


def ensure_database() -> None:
    path = _db_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS waitlist_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                source_page TEXT NOT NULL DEFAULT 'unknown',
                wants_shop_signals INTEGER NOT NULL DEFAULT 0,
                ip_hash TEXT,
                user_agent TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    path = _db_path()
    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
    finally:
        connection.close()
