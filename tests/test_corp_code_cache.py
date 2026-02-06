"""Tests for corp_code_cache module."""

from __future__ import annotations

import io
import zipfile
from unittest.mock import AsyncMock

import pytest

from opendart_fss_mcp.corp_code_cache import CorpCodeCache

# -- Synthetic test data -------------------------------------------------------

_XML_TEMPLATE = """\
<?xml version="1.0" encoding="UTF-8"?>
<result>
{items}
</result>
"""

_ITEM_TEMPLATE = """\
<list>
  <corp_code>{corp_code}</corp_code>
  <corp_name>{corp_name}</corp_name>
  <stock_code>{stock_code}</stock_code>
  <modify_date>{modify_date}</modify_date>
</list>"""

COMPANIES = [
    ("00126380", "삼성전자", "005930", "20240101"),
    ("00164779", "삼성SDI", "006400", "20240101"),
    ("00104842", "삼성생명", "032830", "20240101"),
    ("00401731", "LG전자", "066570", "20240101"),
    ("00356361", "현대자동차", "005380", "20240101"),
    ("99999999", "비상장테스트", "", "20240101"),
    ("88888888", "비상장삼성", "", "20240101"),
]


def _make_zip_bytes() -> bytes:
    items = "\n".join(
        _ITEM_TEMPLATE.format(
            corp_code=c[0], corp_name=c[1], stock_code=c[2], modify_date=c[3]
        )
        for c in COMPANIES
    )
    xml = _XML_TEMPLATE.format(items=items).encode("utf-8")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("CORPCODE.xml", xml)
    return buf.getvalue()


def _mock_client() -> AsyncMock:
    client = AsyncMock()
    client.disclosure.download_corp_codes.return_value = _make_zip_bytes()
    return client


# -- Tests ---------------------------------------------------------------------


@pytest.fixture
def cache() -> CorpCodeCache:
    return CorpCodeCache()


@pytest.mark.asyncio
async def test_load_parses_all_entries(cache: CorpCodeCache) -> None:
    client = _mock_client()
    results = await cache.search(client, "삼성전자")
    assert len(results) == 1
    assert results[0].corp_code == "00126380"
    assert results[0].stock_code == "005930"


@pytest.mark.asyncio
async def test_stock_code_exact_match(cache: CorpCodeCache) -> None:
    client = _mock_client()
    results = await cache.search(client, "005930")
    assert len(results) == 1
    assert results[0].corp_name == "삼성전자"


@pytest.mark.asyncio
async def test_name_exact_match_case_insensitive(cache: CorpCodeCache) -> None:
    client = _mock_client()
    results = await cache.search(client, "lg전자")
    assert len(results) == 1
    assert results[0].corp_name == "LG전자"


@pytest.mark.asyncio
async def test_prefix_match(cache: CorpCodeCache) -> None:
    client = _mock_client()
    results = await cache.search(client, "삼성")
    names = [e.corp_name for e in results]
    assert "삼성전자" in names
    assert "삼성SDI" in names
    assert "삼성생명" in names


@pytest.mark.asyncio
async def test_substring_match(cache: CorpCodeCache) -> None:
    client = _mock_client()
    results = await cache.search(client, "전자")
    names = [e.corp_name for e in results]
    assert "삼성전자" in names
    assert "LG전자" in names


@pytest.mark.asyncio
async def test_search_priority_exact_before_prefix(cache: CorpCodeCache) -> None:
    """Exact name match should come before prefix matches."""
    client = _mock_client()
    results = await cache.search(client, "삼성전자")
    # "삼성전자" is exact, others with "삼성전자" prefix would follow
    assert results[0].corp_name == "삼성전자"


@pytest.mark.asyncio
async def test_search_priority_prefix_before_substring(cache: CorpCodeCache) -> None:
    """Prefix matches for '삼성' should come before substring matches like '비상장삼성'."""
    client = _mock_client()
    results = await cache.search(client, "삼성", max_results=20)
    names = [e.corp_name for e in results]
    # Prefix matches: 삼성전자, 삼성SDI, 삼성생명
    # Substring match: 비상장삼성
    samsung_idx = names.index("삼성전자")
    unlisted_idx = names.index("비상장삼성")
    assert samsung_idx < unlisted_idx


@pytest.mark.asyncio
async def test_listed_only(cache: CorpCodeCache) -> None:
    client = _mock_client()
    results = await cache.search(client, "삼성", listed_only=True, max_results=20)
    for e in results:
        assert e.stock_code is not None
    names = [e.corp_name for e in results]
    assert "비상장삼성" not in names


@pytest.mark.asyncio
async def test_max_results(cache: CorpCodeCache) -> None:
    client = _mock_client()
    results = await cache.search(client, "삼성", max_results=2)
    assert len(results) == 2


@pytest.mark.asyncio
async def test_empty_query(cache: CorpCodeCache) -> None:
    client = _mock_client()
    results = await cache.search(client, "")
    assert results == []


@pytest.mark.asyncio
async def test_no_match(cache: CorpCodeCache) -> None:
    client = _mock_client()
    results = await cache.search(client, "존재하지않는회사")
    assert results == []


@pytest.mark.asyncio
async def test_unlisted_company_stock_code_is_none(cache: CorpCodeCache) -> None:
    client = _mock_client()
    results = await cache.search(client, "비상장테스트")
    assert len(results) == 1
    assert results[0].stock_code is None


@pytest.mark.asyncio
async def test_summary(cache: CorpCodeCache) -> None:
    client = _mock_client()
    summary = await cache.summary(client)
    assert summary["total_count"] == len(COMPANIES)
    assert summary["listed_count"] == 5  # 5 with stock codes
    assert summary["unlisted_count"] == 2


@pytest.mark.asyncio
async def test_cache_reuses_data(cache: CorpCodeCache) -> None:
    """Second search should not trigger another download."""
    client = _mock_client()
    await cache.search(client, "삼성")
    await cache.search(client, "LG")
    client.disclosure.download_corp_codes.assert_awaited_once()


# -- Chosung search tests ------------------------------------------------------


@pytest.mark.asyncio
async def test_chosung_pure_search(cache: CorpCodeCache) -> None:
    """Pure chosung query 'ㅅㅅㅈㅈ' should match 삼성전자."""
    client = _mock_client()
    results = await cache.search(client, "ㅅㅅㅈㅈ")
    names = [e.corp_name for e in results]
    assert "삼성전자" in names


@pytest.mark.asyncio
async def test_chosung_prefix_search(cache: CorpCodeCache) -> None:
    """Chosung prefix 'ㅅㅅ' should match all 삼성* companies."""
    client = _mock_client()
    results = await cache.search(client, "ㅅㅅ", max_results=20)
    names = [e.corp_name for e in results]
    assert "삼성전자" in names
    assert "삼성SDI" in names
    assert "삼성생명" in names


@pytest.mark.asyncio
async def test_chosung_mixed_search(cache: CorpCodeCache) -> None:
    """Mixed chosung+alpha query 'ㅅㅅsdi' should match 삼성SDI."""
    client = _mock_client()
    results = await cache.search(client, "ㅅㅅSDI")
    names = [e.corp_name for e in results]
    assert "삼성SDI" in names


@pytest.mark.asyncio
async def test_chosung_does_not_override_exact(cache: CorpCodeCache) -> None:
    """Exact name match should come before chosung matches."""
    client = _mock_client()
    results = await cache.search(client, "삼성전자")
    assert results[0].corp_name == "삼성전자"


# -- Fuzzy search tests --------------------------------------------------------


@pytest.mark.asyncio
async def test_fuzzy_typo_correction(cache: CorpCodeCache) -> None:
    """Fuzzy matching should correct typo '삼선전자' → 삼성전자."""
    client = _mock_client()
    results = await cache.search(client, "삼선전자")
    names = [e.corp_name for e in results]
    assert "삼성전자" in names


@pytest.mark.asyncio
async def test_fuzzy_no_garbage_results(cache: CorpCodeCache) -> None:
    """Completely unrelated query should not return garbage fuzzy results."""
    client = _mock_client()
    results = await cache.search(client, "xyz무관한쿼리abc")
    assert results == []


@pytest.mark.asyncio
async def test_deterministic_before_fuzzy(cache: CorpCodeCache) -> None:
    """Exact/prefix/substring results must come before fuzzy results."""
    client = _mock_client()
    # "삼성" matches prefix for 삼성전자, 삼성SDI, 삼성생명 and substring for 비상장삼성
    # Fuzzy results (if any) should come after these
    results = await cache.search(client, "삼성", max_results=20)
    names = [e.corp_name for e in results]
    prefix_names = {"삼성전자", "삼성SDI", "삼성생명"}
    # All prefix matches should appear before any non-prefix/non-substring match
    prefix_indices = [names.index(n) for n in prefix_names if n in names]
    other_indices = [
        i for i, n in enumerate(names) if n not in prefix_names and n != "비상장삼성"
    ]
    if prefix_indices and other_indices:
        assert max(prefix_indices) < min(other_indices)


@pytest.mark.asyncio
async def test_chosung_entry_field_computed(cache: CorpCodeCache) -> None:
    """Verify that corp_name_chosung is precomputed on load."""
    client = _mock_client()
    await cache.search(client, "삼성")  # trigger load
    entry = next(e for e in cache._entries if e.corp_name == "삼성전자")
    assert entry.corp_name_chosung == "ㅅㅅㅈㅈ"
