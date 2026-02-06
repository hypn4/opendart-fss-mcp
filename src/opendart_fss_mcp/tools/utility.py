"""유틸리티 - Utility tools."""

from datetime import datetime
from zoneinfo import ZoneInfo

from fastmcp import FastMCP

mcp = FastMCP(name="Utility")

TOOL_ANNOTATIONS = {"readOnlyHint": True}
TAGS = {"utility"}

KST = ZoneInfo("Asia/Seoul")


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
def get_current_date() -> dict:
    """현재 날짜와 시간을 한국 표준시(KST) 기준으로 반환합니다.

    날짜가 필요한 다른 도구를 호출하기 전에 이 도구를 먼저 사용하세요.
    """
    now = datetime.now(KST)
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "timezone": "Asia/Seoul (KST)",
    }
