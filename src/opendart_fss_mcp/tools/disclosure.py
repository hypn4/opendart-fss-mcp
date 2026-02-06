"""공시정보 (DS001) - Disclosure Information tools."""

from typing import Annotated

from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from opendart_fss_mcp.corp_code_cache import get_cache
from opendart_fss_mcp.deps import call_api, get_client, to_dict

mcp = FastMCP(name="Disclosure")

TOOL_ANNOTATIONS = {"readOnlyHint": True, "openWorldHint": True}
TAGS = {"disclosure"}


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def search_company(
    query: Annotated[
        str, Field(description="회사명 또는 종목코드 (예: '삼성전자', '005930')")
    ],
    max_results: Annotated[int, Field(description="최대 결과 수")] = 10,
    listed_only: Annotated[bool, Field(description="상장회사만 검색")] = False,
    client=Depends(get_client),
) -> list[dict]:
    """회사명 또는 종목코드로 고유번호(corp_code)를 검색합니다.

    다른 도구에서 corp_code가 필요할 때, 먼저 이 도구로 회사를 검색하세요.
    """
    cache = get_cache()
    entries = await cache.search(
        client, query, max_results=max_results, listed_only=listed_only
    )
    return [
        {
            "corp_code": e.corp_code,
            "corp_name": e.corp_name,
            "stock_code": e.stock_code,
            "modify_date": e.modify_date,
        }
        for e in entries
    ]


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def search(
    corp_code: Annotated[str | None, Field(description="고유번호 (8자리)")] = None,
    bgn_de: Annotated[str | None, Field(description="시작일 (YYYYMMDD)")] = None,
    end_de: Annotated[str | None, Field(description="종료일 (YYYYMMDD)")] = None,
    last_reprt_at: Annotated[
        str | None, Field(description="최종보고서 검색여부 (Y/N)")
    ] = None,
    pblntf_ty: Annotated[str | None, Field(description="공시유형 (A~J)")] = None,
    pblntf_detail_ty: Annotated[str | None, Field(description="공시상세유형")] = None,
    corp_cls: Annotated[
        str | None, Field(description="법인구분 (Y:유가, K:코스닥, N:코넥스, E:기타)")
    ] = None,
    sort: Annotated[str | None, Field(description="정렬키 (date, crp, rpt)")] = None,
    sort_mth: Annotated[str | None, Field(description="정렬방법 (asc, desc)")] = None,
    page_no: Annotated[int | None, Field(description="페이지 번호")] = None,
    page_count: Annotated[int | None, Field(description="페이지 당 건수")] = None,
    client=Depends(get_client),
) -> list[dict]:
    """공시 정보를 검색합니다."""
    result = await call_api(
        client.disclosure.search(
            corp_code=corp_code,
            bgn_de=bgn_de,
            end_de=end_de,
            last_reprt_at=last_reprt_at,
            pblntf_ty=pblntf_ty,
            pblntf_detail_ty=pblntf_detail_ty,
            corp_cls=corp_cls,
            sort=sort,
            sort_mth=sort_mth,
            page_no=page_no,
            page_count=page_count,
        )
    )
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def company(
    corp_code: Annotated[str, Field(description="고유번호 (8자리)")],
    client=Depends(get_client),
) -> dict:
    """기업 개황 정보를 조회합니다."""
    result = await call_api(client.disclosure.get_company(corp_code=corp_code))
    return to_dict(result)


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def document(
    rcept_no: Annotated[str, Field(description="접수번호 (14자리)")],
    client=Depends(get_client),
) -> str:
    """공시 원문 문서를 다운로드합니다. ZIP 파일의 바이트를 반환합니다."""
    result = await call_api(client.disclosure.download_document(rcept_no=rcept_no))
    return f"ZIP 파일 다운로드 완료 ({len(result)} bytes)"


@mcp.tool(tags=TAGS, annotations=TOOL_ANNOTATIONS)
async def corp_codes(
    client=Depends(get_client),
) -> dict:
    """고유번호 목록을 로드하고 요약 정보를 반환합니다."""
    cache = get_cache()
    return await cache.summary(client)
