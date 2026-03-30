"""Shared dependencies -- Supabase client, auth, cost tracking."""
import logging
import os
from functools import lru_cache

from dotenv import load_dotenv
from fastapi import Header, HTTPException
from supabase import create_client, Client

load_dotenv()

logger = logging.getLogger("costimize")

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]


@lru_cache()
def get_supabase_admin() -> Client:
    """Service role client -- bypasses RLS. For backend writes only."""
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


@lru_cache()
def get_supabase_client() -> Client:
    """Anon client -- respects RLS. For user-scoped reads."""
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


async def get_current_user_id(authorization: str = Header(...)) -> str:
    """Extract user ID from Supabase JWT in Authorization header."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.split(" ", 1)[1]
    client = get_supabase_client()

    try:
        user_response = client.auth.get_user(token)
        if user_response and user_response.user:
            return user_response.user.id
    except Exception as exc:
        logger.warning("Auth validation failed: %s", exc)

    raise HTTPException(status_code=401, detail="Invalid or expired token")
