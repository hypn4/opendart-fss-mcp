"""OpenDartClient dependency injection and API error handling."""

from __future__ import annotations

from typing import Any

import msgspec
from fastmcp.exceptions import ToolError
from opendart_fss import OpenDartClient
from opendart_fss.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)

_client: OpenDartClient | None = None
_api_key: str | None = None


def configure(api_key: str | None) -> None:
    """Set the API key before server startup."""
    global _api_key
    _api_key = api_key


def get_client() -> OpenDartClient:
    """Dependency for tool functions. Injected via Depends().

    Lazily creates a singleton OpenDartClient on first use.
    """
    global _client
    if _client is None:
        _client = OpenDartClient(api_key=_api_key)
    return _client


async def call_api(coro):  # noqa: ANN001
    """Wrap SDK calls and convert exceptions to ToolError."""
    try:
        return await coro
    except AuthenticationError as e:
        raise ToolError(f"인증 실패: API Key를 확인하세요. ({e})") from e
    except RateLimitError as e:
        raise ToolError(f"요청 한도 초과: 잠시 후 재시도하세요. ({e})") from e
    except ValidationError as e:
        raise ToolError(f"파라미터 오류: {e}") from e
    except NotFoundError as e:
        raise ToolError(f"데이터 없음: {e}") from e
    except ServerError as e:
        raise ToolError(f"OpenDART 서버 오류: {e}") from e


def to_dict(obj: object) -> Any:
    """Convert msgspec.Struct responses to JSON-serializable dicts."""
    return msgspec.to_builtins(obj)
