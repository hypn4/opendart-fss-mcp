"""증권신고서 (DS006) - Securities Registration tools."""

from typing import Annotated

from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from opendart_fss_mcp.deps import call_api, get_client, to_dict

mcp = FastMCP(name="Registration")

TOOL_ANNOTATIONS = {"readOnlyHint": True, "openWorldHint": True}
TAGS = {"registration"}


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def equity_securities(
    corp_code: Annotated[str, Field(description="고유번호 (8자리)")],
    bgn_de: Annotated[str | None, Field(description="시작일 (YYYYMMDD)")] = None,
    end_de: Annotated[str | None, Field(description="종료일 (YYYYMMDD)")] = None,
    client=Depends(get_client),
) -> list[dict]:
    """지분증권 발행 신고서를 조회합니다."""
    result = await call_api(
        client.registration.get_equity_securities(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def debt_securities(
    corp_code: Annotated[str, Field(description="고유번호 (8자리)")],
    bgn_de: Annotated[str | None, Field(description="시작일 (YYYYMMDD)")] = None,
    end_de: Annotated[str | None, Field(description="종료일 (YYYYMMDD)")] = None,
    client=Depends(get_client),
) -> list[dict]:
    """채무증권 발행 신고서를 조회합니다."""
    result = await call_api(
        client.registration.get_debt_securities(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def merger_registration(
    corp_code: Annotated[str, Field(description="고유번호 (8자리)")],
    bgn_de: Annotated[str | None, Field(description="시작일 (YYYYMMDD)")] = None,
    end_de: Annotated[str | None, Field(description="종료일 (YYYYMMDD)")] = None,
    client=Depends(get_client),
) -> list[dict]:
    """합병 신고서를 조회합니다."""
    result = await call_api(
        client.registration.get_merger_registration(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def split_registration(
    corp_code: Annotated[str, Field(description="고유번호 (8자리)")],
    bgn_de: Annotated[str | None, Field(description="시작일 (YYYYMMDD)")] = None,
    end_de: Annotated[str | None, Field(description="종료일 (YYYYMMDD)")] = None,
    client=Depends(get_client),
) -> list[dict]:
    """분할 신고서를 조회합니다."""
    result = await call_api(
        client.registration.get_split_registration(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def depositary_receipt(
    corp_code: Annotated[str, Field(description="고유번호 (8자리)")],
    bgn_de: Annotated[str | None, Field(description="시작일 (YYYYMMDD)")] = None,
    end_de: Annotated[str | None, Field(description="종료일 (YYYYMMDD)")] = None,
    client=Depends(get_client),
) -> list[dict]:
    """예탁증권 신고서를 조회합니다."""
    result = await call_api(
        client.registration.get_depositary_receipt(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def stock_exchange_transfer(
    corp_code: Annotated[str, Field(description="고유번호 (8자리)")],
    bgn_de: Annotated[str | None, Field(description="시작일 (YYYYMMDD)")] = None,
    end_de: Annotated[str | None, Field(description="종료일 (YYYYMMDD)")] = None,
    client=Depends(get_client),
) -> list[dict]:
    """주식교환이전 신고서를 조회합니다."""
    result = await call_api(
        client.registration.get_stock_exchange_transfer(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)
