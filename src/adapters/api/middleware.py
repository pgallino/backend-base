import json
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.log import logger, new_request_id, request_id_ctx_var


def add_middlewares(app: FastAPI, settings: Any) -> None:
    """Configure CORS (if requested) and add the request-id middleware.

    This centralizes the middleware configuration so `src/app.py` stays small.
    """
    raw = getattr(settings, "ALLOWED_ORIGINS", None) or ""
    allow_all = getattr(settings, "ALLOW_ALL_ORIGINS", False)

    origins = []
    if allow_all:
        origins = ["*"]
    else:
        if raw:
            ra = raw.strip()
            if ra.startswith("["):
                try:
                    origins = json.loads(ra)
                except Exception:
                    origins = [
                        o.strip() for o in ra.strip("[]").split(",") if o.strip()
                    ]
            else:
                origins = [o.strip() for o in ra.split(",") if o.strip()]

    if not origins and getattr(settings, "ENVIRONMENT", "") in ("dev", "development"):
        origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

    if origins:
        allow_credentials = not (len(origins) == 1 and origins[0] == "*")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=allow_credentials,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["Authorization", "Content-Type", "Accept"],
            max_age=3600,
        )
        logger.debug(
            "CORS configured origins=%s allow_credentials=%s",
            origins,
            allow_credentials,
        )

    @app.middleware("http")
    async def add_request_id_middleware(request: Request, call_next):
        """Ensure a request id exists for every request and populate the log context."""
        rid = request.headers.get("X-Request-ID") or new_request_id()
        request_id_ctx_var.set(rid)
        logger.debug(
            "HTTP request start %s %s request_id=%s",
            request.method,
            request.url.path,
            rid,
        )
        try:
            response = await call_next(request)
        finally:
            request_id_ctx_var.set("-")
        response.headers["X-Request-ID"] = rid
        logger.debug(
            "HTTP request end %s %s request_id=%s status=%s",
            request.method,
            request.url.path,
            rid,
            getattr(response, "status_code", "-"),
        )
        return response
