from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "Wallyverse Core API"
    app_env: str = os.getenv("WALLYVERSE_ENV", "development")
    db_path: str = os.getenv("WALLYVERSE_DB_PATH", "./data/wallyverse.db")
    ip_hash_salt: str = os.getenv("WALLYVERSE_IP_HASH_SALT", "wallyverse-local-salt")
    shops_count_teaser: int = int(os.getenv("WALLYVERSE_SHOPS_COUNT_TEASER", "3"))
    cors_origins: tuple[str, ...] = tuple(
        origin.strip()
        for origin in os.getenv(
            "WALLYVERSE_CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        ).split(",")
        if origin.strip()
    )


settings = Settings()
