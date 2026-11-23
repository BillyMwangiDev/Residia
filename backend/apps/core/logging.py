from __future__ import annotations

from contextvars import ContextVar

request_id_context: ContextVar[str] = ContextVar("request_id", default="-")
user_id_context: ContextVar[str] = ContextVar("user_id", default="anonymous")


class RequestContextFilter:
    """Attach request context values to log records."""

    def filter(self, record) -> bool:
        record.request_id = request_id_context.get()
        record.user_id = user_id_context.get()
        return True
