import os
import ssl
from typing import Any, Dict, Union
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# default to sqlite for local development
DB_URL = os.getenv("DB_URL_ASYNC", "sqlite+aiosqlite:///./dev.db")


def _sanitize_async_url_and_connect_args(db_url: str):
    """Remove any ``sslmode`` query param from the URL and return
    (sanitized_url, connect_args).

    asyncpg's connect() does not accept the ``sslmode`` keyword argument
    (that's used by sync drivers like psycopg2). If a connection string
    includes ``?sslmode=require`` (for example from Neon), we translate
    that into a proper ``ssl`` argument for asyncpg (an SSLContext).
    """
    try:
        parsed = urlparse(db_url)
    except Exception:
        return db_url, {}

    if not parsed.query:
        return db_url, {}

    qs = dict(parse_qsl(parsed.query, keep_blank_values=True))
    sslmode = None
    # support both lowercase and uppercase keys just in case
    for key in ("sslmode", "SSL_MODE", "ssl_mode"):
        if key in qs:
            sslmode = qs.pop(key)
            break

    if sslmode is None:
        return db_url, {}

    # rebuild URL without sslmode
    new_query = urlencode(qs, doseq=True)
    sanitized = urlunparse(parsed._replace(query=new_query))

    # Map sslmode values to an SSLContext (asyncpg expects 'ssl')
    ssl_arg: Union[bool, ssl.SSLContext, None] = None
    if sslmode.lower() == "disable":
        ssl_arg = False
    else:
        # create a default SSL context which enforces cert verification
        ctx = ssl.create_default_context()
        ssl_arg = ctx

    return sanitized, {"ssl": ssl_arg}


sanitized_url, _connect_args = _sanitize_async_url_and_connect_args(DB_URL)

engine = create_async_engine(
    sanitized_url, connect_args=_connect_args, echo=True, future=True
)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
