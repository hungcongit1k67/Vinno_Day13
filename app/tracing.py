from __future__ import annotations

import json
import os
from typing import Any

try:
    from langfuse import observe, get_client, LangfuseOtelSpanAttributes
    from opentelemetry import trace as otel_trace

    class _LangfuseContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            try:
                span = otel_trace.get_current_span()
                if user_id := kwargs.get("user_id"):
                    span.set_attribute(LangfuseOtelSpanAttributes.TRACE_USER_ID, user_id)
                if session_id := kwargs.get("session_id"):
                    span.set_attribute(LangfuseOtelSpanAttributes.TRACE_SESSION_ID, session_id)
                if tags := kwargs.get("tags"):
                    span.set_attribute(LangfuseOtelSpanAttributes.TRACE_TAGS, json.dumps(tags))
            except Exception:
                pass

        def update_current_observation(self, **kwargs: Any) -> None:
            try:
                metadata = kwargs.get("metadata")
                usage_details = kwargs.get("usage_details")
                get_client().update_current_span(
                    metadata=metadata,
                    **({"usage": usage_details} if usage_details else {}),
                )
            except Exception:
                pass

    langfuse_context = _LangfuseContext()

except Exception:  # pragma: no cover
    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    class _DummyContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None

        def update_current_observation(self, **kwargs: Any) -> None:
            return None

    langfuse_context = _DummyContext()


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))
