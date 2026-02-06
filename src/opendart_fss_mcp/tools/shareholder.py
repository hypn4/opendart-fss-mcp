"""지분공시 (DS004) - Shareholding Information tools."""

from typing import Annotated

from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from opendart_fss_mcp.deps import call_api, get_client, to_dict

mcp = FastMCP(name="Shareholder")

TOOL_ANNOTATIONS = {"readOnlyHint": True, "openWorldHint": True}
TAGS = {"shareholder"}


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def major_stock(
    corp_code: Annotated[str, Field(description="고유번호 (8자리)")],
    client=Depends(get_client),
) -> list[dict]:
    """대량보유 현황을 조회합니다."""
    result = await call_api(client.shareholder.get_major_stock(corp_code=corp_code))
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def executive_stock(
    corp_code: Annotated[str, Field(description="고유번호 (8자리)")],
    client=Depends(get_client),
) -> list[dict]:
    """임원 및 주요주주 소유 현황을 조회합니다."""
    result = await call_api(client.shareholder.get_executive_stock(corp_code=corp_code))
    return to_dict(result)
