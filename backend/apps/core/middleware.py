from __future__ import annotations

import uuid

from .logging import request_id_context, user_id_context


class RequestContextMiddleware:
    """Expose request metadata to structured logs."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        user_id = (
            str(request.user.pk)
            if getattr(request, "user", None) and request.user.is_authenticated
            else "anonymous"
        )

        request_token = request_id_context.set(request_id)
        user_token = user_id_context.set(user_id)
        try:
            response = self.get_response(request)
            response["X-Request-ID"] = request_id
            return response
        finally:
            request_id_context.reset(request_token)
            user_id_context.reset(user_token)
