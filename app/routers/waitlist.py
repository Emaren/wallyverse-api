from __future__ import annotations

import hashlib
import sqlite3
from datetime import datetime, timezone

from fastapi import APIRouter, Request, Response, status

from ..config import settings
from ..db import get_connection
from ..schemas import WaitlistCreate, WaitlistResponse, WaitlistStats

router = APIRouter(prefix="/v1", tags=["waitlist"])


@router.post("/waitlist", response_model=WaitlistResponse, status_code=status.HTTP_201_CREATED)
def create_waitlist_entry(
    payload: WaitlistCreate,
    request: Request,
    response: Response,
) -> WaitlistResponse:
    client_ip = request.client.host if request.client else "unknown"
    hashed_ip = hashlib.sha256(f"{client_ip}:{settings.ip_hash_salt}".encode("utf-8")).hexdigest()[:24]
    user_agent = request.headers.get("user-agent", "unknown")[:200]

    with get_connection() as connection:
        try:
            connection.execute(
                """
                INSERT INTO waitlist_entries (email, source_page, wants_shop_signals, ip_hash, user_agent)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    payload.email.lower(),
                    payload.source_page.strip().lower(),
                    int(payload.wants_shop_signals),
                    hashed_ip,
                    user_agent,
                ),
            )
            connection.commit()
        except sqlite3.IntegrityError as exc:
            if "UNIQUE constraint failed" in str(exc):
                response.status_code = status.HTTP_200_OK
                return WaitlistResponse(
                    message="Already on the scroll. Watch the skies.",
                    created=False,
                )
            raise

    return WaitlistResponse(
        message="You're on the scroll. Watch the skies.",
        created=True,
    )


@router.get("/stats", response_model=WaitlistStats)
def get_stats() -> WaitlistStats:
    with get_connection() as connection:
        row = connection.execute("SELECT COUNT(*) AS count FROM waitlist_entries").fetchone()

    return WaitlistStats(
        waitlist_count=int(row["count"] if row else 0),
        shops_count_teaser=settings.shops_count_teaser,
        as_of=datetime.now(timezone.utc),
    )
