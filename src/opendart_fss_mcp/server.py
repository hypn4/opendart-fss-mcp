"""OpenDART FSS MCP Server."""

from __future__ import annotations

import asyncio

from fastmcp import FastMCP
from starlette.responses import JSONResponse

from opendart_fss_mcp.tools import (
    disclosure,
    financial,
    major_event,
    registration,
    report,
    shareholder,
    utility,
)

try:
    from opendart_fss_mcp._version import __version__
except ImportError:
    __version__ = "0.0.0.dev0"

mcp = FastMCP(
    name="OpenDART",
    instructions=(
        "한국 금융감독원 전자공시시스템(DART) API를 통해 "
        "기업 공시, 재무제표, 지분, 주요사항 등을 조회합니다.\n\n"
        "## 중요: 오늘 날짜 확인\n"
        "날짜 관련 작업 전에 반드시 `utility_get_current_date` 도구로 "
        "오늘 날짜를 확인하세요.\n\n"
        "## 중요: 회사 검색 워크플로우\n"
        "대부분의 도구는 corp_code(고유번호, 8자리)를 필요로 합니다.\n"
        "사용자가 회사명이나 종목코드를 제공한 경우, "
        "반드시 먼저 `disclosure_search_company` 도구로 corp_code를 조회하세요.\n"
        "예: '삼성전자 재무제표 보여줘' → disclosure_search_company('삼성전자') → "
        "corp_code 획득 → financial_single_account(corp_code=...) 호출"
    ),
    version=__version__,
    on_duplicate_tools="error",
)


@mcp.custom_route("/health", methods=["GET"])
async def health(request: object) -> JSONResponse:
    return JSONResponse(
        {"status": "ok", "service": "opendart-mcp", "version": __version__}
    )


_SERVERS = [
    (disclosure.mcp, "disclosure"),
    (financial.mcp, "financial"),
    (report.mcp, "report"),
    (shareholder.mcp, "shareholder"),
    (major_event.mcp, "event"),
    (registration.mcp, "registration"),
    (utility.mcp, "utility"),
]


async def _setup() -> None:
    for sub_server, prefix in _SERVERS:
        await mcp.import_server(sub_server, prefix=prefix)


asyncio.run(_setup())
