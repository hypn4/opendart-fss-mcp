"""정기보고서 (DS002) - Regular Report Key Information tools."""

from typing import Annotated

from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from opendart_fss_mcp.deps import call_api, get_client, to_dict

mcp = FastMCP(name="Report")

TOOL_ANNOTATIONS = {"readOnlyHint": True, "openWorldHint": True}
TAGS = {"report"}

CORP_CODE = Annotated[str, Field(description="고유번호 (8자리)")]
BSNS_YEAR = Annotated[str, Field(description="사업연도 (YYYY)")]
REPRT_CODE = Annotated[
    str,
    Field(description="보고서코드 (11011:사업, 11012:반기, 11013:1분기, 11014:3분기)"),
]


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def stock_changes(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """증자/감자 현황을 조회합니다."""
    result = await call_api(
        client.report.get_stock_changes(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def dividends(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """배당 정보를 조회합니다."""
    result = await call_api(
        client.report.get_dividends(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def treasury_stock(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """자기주식 현황을 조회합니다."""
    result = await call_api(
        client.report.get_treasury_stock(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def largest_shareholders(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """최대주주 현황을 조회합니다."""
    result = await call_api(
        client.report.get_largest_shareholders(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def largest_shareholder_changes(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """최대주주 변동 현황을 조회합니다."""
    result = await call_api(
        client.report.get_largest_shareholder_changes(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def minority_shareholders(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """소액주주 현황을 조회합니다."""
    result = await call_api(
        client.report.get_minority_shareholders(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def executives(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """임원 현황을 조회합니다."""
    result = await call_api(
        client.report.get_executives(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def employees(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """직원 현황을 조회합니다."""
    result = await call_api(
        client.report.get_employees(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def individual_compensation(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """개인별 보수를 조회합니다."""
    result = await call_api(
        client.report.get_individual_compensation(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def director_compensation(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """이사 보수를 조회합니다."""
    result = await call_api(
        client.report.get_director_compensation(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def director_individual_compensation(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """이사 개인별 보수를 조회합니다."""
    result = await call_api(
        client.report.get_director_individual_compensation(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def unregistered_executive_compensation(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """미등기 임원 보수를 조회합니다."""
    result = await call_api(
        client.report.get_unregistered_executive_compensation(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def director_compensation_approval(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """이사 보수 승인 현황을 조회합니다."""
    result = await call_api(
        client.report.get_director_compensation_approval(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def director_compensation_by_type(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """유형별 이사 보수를 조회합니다."""
    result = await call_api(
        client.report.get_director_compensation_by_type(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def other_corp_investments(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """타법인 출자 현황을 조회합니다."""
    result = await call_api(
        client.report.get_other_corp_investments(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def total_stock_quantity(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """주식 총수 현황을 조회합니다."""
    result = await call_api(
        client.report.get_total_stock_quantity(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def debt_securities_issuance(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """채무증권 발행실적을 조회합니다."""
    result = await call_api(
        client.report.get_debt_securities_issuance(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def commercial_paper_balance(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """기업어음 잔액을 조회합니다."""
    result = await call_api(
        client.report.get_commercial_paper_balance(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def short_term_bond_balance(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """단기사채 잔액을 조회합니다."""
    result = await call_api(
        client.report.get_short_term_bond_balance(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def corporate_bond_balance(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """회사채 잔액을 조회합니다."""
    result = await call_api(
        client.report.get_corporate_bond_balance(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def hybrid_securities_balance(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """조건부자본증권 잔액을 조회합니다."""
    result = await call_api(
        client.report.get_hybrid_securities_balance(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def contingent_capital_balance(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """신종자본증권 잔액을 조회합니다."""
    result = await call_api(
        client.report.get_contingent_capital_balance(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def auditor_opinion(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """감사 의견을 조회합니다."""
    result = await call_api(
        client.report.get_auditor_opinion(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def audit_service_contract(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """감사 용역 계약 현황을 조회합니다."""
    result = await call_api(
        client.report.get_audit_service_contract(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def non_audit_service_contract(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """비감사 용역 계약 현황을 조회합니다."""
    result = await call_api(
        client.report.get_non_audit_service_contract(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def outside_directors(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """사외이사 현황을 조회합니다."""
    result = await call_api(
        client.report.get_outside_directors(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def public_offering_fund_usage(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """공모자금 사용 현황을 조회합니다."""
    result = await call_api(
        client.report.get_public_offering_fund_usage(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def private_placement_fund_usage(
    corp_code: CORP_CODE,
    bsns_year: BSNS_YEAR,
    reprt_code: REPRT_CODE,
    client=Depends(get_client),
) -> list[dict]:
    """사모자금 사용 현황을 조회합니다."""
    result = await call_api(
        client.report.get_private_placement_fund_usage(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    return to_dict(result)
