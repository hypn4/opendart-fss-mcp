"""재무정보 (DS003) - Financial Information tools."""

from typing import Annotated

from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from opendart_fss_mcp.deps import call_api, get_client, to_dict

mcp = FastMCP(name="Financial")

TOOL_ANNOTATIONS = {"readOnlyHint": True, "openWorldHint": True}
TAGS = {"financial"}


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def single_account(
    corp_code: Annotated[str, Field(description="고유번호 (8자리)")],
    bsns_year: Annotated[str, Field(description="사업연도 (YYYY)")],
    reprt_code: Annotated[
        str,
        Field(
            description="보고서코드 (11011:사업, 11012:반기, 11013:1분기, 11014:3분기)"
        ),
    ],
    fs_div: Annotated[
        str, Field(description="재무제표구분 (CFS:연결, OFS:개별)")
    ] = "CFS",
    client=Depends(get_client),
) -> list[dict]:
    """단일 기업의 주요 재무 계정을 조회합니다."""
    result = await call_api(
        client.financial.get_single_account(
            corp_code=corp_code,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
            fs_div=fs_div,
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def multi_account(
    corp_code: Annotated[str, Field(description="고유번호 (쉼표 구분, 최대 20개)")],
    bsns_year: Annotated[str, Field(description="사업연도 (YYYY)")],
    reprt_code: Annotated[
        str,
        Field(
            description="보고서코드 (11011:사업, 11012:반기, 11013:1분기, 11014:3분기)"
        ),
    ],
    fs_div: Annotated[
        str, Field(description="재무제표구분 (CFS:연결, OFS:개별)")
    ] = "CFS",
    client=Depends(get_client),
) -> list[dict]:
    """복수 기업의 주요 재무 계정을 조회합니다."""
    result = await call_api(
        client.financial.get_multi_account(
            corp_code=corp_code,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
            fs_div=fs_div,
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def full_statements(
    corp_code: Annotated[str, Field(description="고유번호 (8자리)")],
    bsns_year: Annotated[str, Field(description="사업연도 (YYYY)")],
    reprt_code: Annotated[
        str,
        Field(
            description="보고서코드 (11011:사업, 11012:반기, 11013:1분기, 11014:3분기)"
        ),
    ],
    fs_div: Annotated[
        str, Field(description="재무제표구분 (CFS:연결, OFS:개별)")
    ] = "CFS",
    client=Depends(get_client),
) -> list[dict]:
    """전체 재무제표를 조회합니다."""
    result = await call_api(
        client.financial.get_full_statements(
            corp_code=corp_code,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
            fs_div=fs_div,
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def xbrl_download(
    rcept_no: Annotated[str, Field(description="접수번호 (14자리)")],
    reprt_code: Annotated[
        str,
        Field(
            description="보고서코드 (11011:사업, 11012:반기, 11013:1분기, 11014:3분기)"
        ),
    ],
    client=Depends(get_client),
) -> str:
    """XBRL 파일을 다운로드합니다."""
    result = await call_api(
        client.financial.download_xbrl(rcept_no=rcept_no, reprt_code=reprt_code)
    )
    return f"XBRL 파일 다운로드 완료 ({len(result)} bytes)"


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def xbrl_taxonomy(
    sj_div: Annotated[
        str,
        Field(
            description="재무제표구분 (BS:재무상태표, IS:손익계산서, CIS:포괄손익계산서, CF:현금흐름표, SCE:자본변동표)"
        ),
    ],
    client=Depends(get_client),
) -> list[dict]:
    """XBRL 택소노미를 조회합니다."""
    result = await call_api(client.financial.get_xbrl_taxonomy(sj_div=sj_div))
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def indicators(
    corp_code: Annotated[str, Field(description="고유번호 (쉼표 구분, 최대 20개)")],
    bsns_year: Annotated[str, Field(description="사업연도 (YYYY)")],
    reprt_code: Annotated[
        str,
        Field(
            description="보고서코드 (11011:사업, 11012:반기, 11013:1분기, 11014:3분기)"
        ),
    ],
    idx_cl_code: Annotated[str | None, Field(description="지표분류코드")] = None,
    client=Depends(get_client),
) -> list[dict]:
    """복수 기업의 재무 지표를 조회합니다."""
    result = await call_api(
        client.financial.get_indicators(
            corp_code=corp_code,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
            idx_cl_code=idx_cl_code,
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def single_indicators(
    corp_code: Annotated[str, Field(description="고유번호 (8자리)")],
    bsns_year: Annotated[str, Field(description="사업연도 (YYYY)")],
    reprt_code: Annotated[
        str,
        Field(
            description="보고서코드 (11011:사업, 11012:반기, 11013:1분기, 11014:3분기)"
        ),
    ],
    idx_cl_code: Annotated[str, Field(description="지표분류코드")],
    client=Depends(get_client),
) -> list[dict]:
    """단일 기업의 재무 지표를 조회합니다."""
    result = await call_api(
        client.financial.get_single_indicators(
            corp_code=corp_code,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
            idx_cl_code=idx_cl_code,
        )
    )
    return to_dict(result)
