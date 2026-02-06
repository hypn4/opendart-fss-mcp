"""주요사항 (DS005) - Major Events tools."""

from typing import Annotated

from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from opendart_fss_mcp.deps import call_api, get_client, to_dict

mcp = FastMCP(name="MajorEvent")

TOOL_ANNOTATIONS = {"readOnlyHint": True, "openWorldHint": True}
TAGS = {"major_event"}

CORP_CODE = Annotated[str, Field(description="고유번호 (8자리)")]
BGN_DE = Annotated[str | None, Field(description="시작일 (YYYYMMDD)")]
END_DE = Annotated[str | None, Field(description="종료일 (YYYYMMDD)")]


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def paid_capital_increase(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """유상증자 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_paid_capital_increase(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def bonus_issue(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """무상증자 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_bonus_issue(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def capital_reduction(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """감자 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_capital_reduction(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def mixed_capital_increase(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """유무상증자 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_mixed_capital_increase(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def convertible_bond(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """전환사채 발행 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_convertible_bond(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def bond_with_warrant(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """신주인수권부사채 발행 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_bond_with_warrant(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def exchangeable_bond(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """교환사채 발행 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_exchangeable_bond(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def merger_decision(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """합병 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_merger_decision(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def split_decision(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """분할 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_split_decision(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def split_merger_decision(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """분할합병 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_split_merger_decision(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def stock_exchange_decision(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """주식의 포괄적 교환·이전 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_stock_exchange_decision(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def asset_transfer(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """영업양수도 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_asset_transfer(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def business_acquisition(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """영업양수 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_business_acquisition(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def business_disposal(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """영업양도 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_business_disposal(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def tangible_asset_acquisition(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """유형자산 양수 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_tangible_asset_acquisition(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def tangible_asset_disposal(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """유형자산 양도 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_tangible_asset_disposal(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def other_corp_stock_acquisition(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """타법인 주식 및 출자증권 양수 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_other_corp_stock_acquisition(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def other_corp_stock_disposal(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """타법인 주식 및 출자증권 양도 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_other_corp_stock_disposal(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def stock_related_bond_acquisition(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """주권 관련 사채권 양수 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_stock_related_bond_acquisition(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def stock_related_bond_disposal(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """주권 관련 사채권 양도 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_stock_related_bond_disposal(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def treasury_stock_acquisition(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """자기주식 취득 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_treasury_stock_acquisition(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def treasury_stock_disposal(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """자기주식 처분 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_treasury_stock_disposal(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def treasury_trust_contract(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """자기주식취득 신탁계약 체결 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_treasury_trust_contract(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def treasury_trust_termination(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """자기주식취득 신탁계약 해지 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_treasury_trust_termination(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def default_occurrence(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """채무불이행을 조회합니다."""
    result = await call_api(
        client.major_event.get_default_occurrence(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def business_suspension(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """영업정지를 조회합니다."""
    result = await call_api(
        client.major_event.get_business_suspension(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def rehabilitation_filing(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """회생절차 신청을 조회합니다."""
    result = await call_api(
        client.major_event.get_rehabilitation_filing(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def dissolution_reason(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """해산 사유를 조회합니다."""
    result = await call_api(
        client.major_event.get_dissolution_reason(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def creditor_management_start(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """채권자관리절차 개시를 조회합니다."""
    result = await call_api(
        client.major_event.get_creditor_management_start(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def creditor_management_stop(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """채권자관리절차 중단을 조회합니다."""
    result = await call_api(
        client.major_event.get_creditor_management_stop(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def write_off_contingent_capital(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """상각형 조건부자본증권 발행 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_write_off_contingent_capital(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def litigation(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """소송을 조회합니다."""
    result = await call_api(
        client.major_event.get_litigation(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def overseas_listing_decision(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """해외상장 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_overseas_listing_decision(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def overseas_delisting_decision(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """해외상장폐지 결정을 조회합니다."""
    result = await call_api(
        client.major_event.get_overseas_delisting_decision(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def overseas_listing(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """해외상장을 조회합니다."""
    result = await call_api(
        client.major_event.get_overseas_listing(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def overseas_delisting(
    corp_code: CORP_CODE,
    bgn_de: BGN_DE = None,
    end_de: END_DE = None,
    client=Depends(get_client),
) -> list[dict]:
    """해외상장폐지를 조회합니다."""
    result = await call_api(
        client.major_event.get_overseas_delisting(
            corp_code=corp_code, bgn_de=bgn_de, end_de=end_de
        )
    )
    return to_dict(result)
