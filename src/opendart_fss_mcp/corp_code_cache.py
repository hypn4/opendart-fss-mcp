"""Corp code cache: ZIP download, XML parsing, in-memory cache, and search."""

from __future__ import annotations

import asyncio
import io
import time
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass

from opendart_fss import OpenDartClient

from opendart_fss_mcp.korean import (
    extract_chosung,
    has_chosung,
    normalize_mixed_query,
)

_TTL_SECONDS = 24 * 60 * 60  # 24 hours


@dataclass(slots=True)
class CorpCodeEntry:
    corp_code: str
    corp_name: str
    corp_name_lower: str  # pre-lowered for search
    corp_name_chosung: str  # pre-computed chosung (e.g. "ㅅㅅㅈㅈ")
    stock_code: str | None
    modify_date: str | None


class CorpCodeCache:
    """Lazy-loaded, TTL-based in-memory cache for DART corp codes."""

    def __init__(self) -> None:
        self._entries: list[CorpCodeEntry] = []
        self._by_stock_code: dict[str, CorpCodeEntry] = {}
        self._by_name_lower: dict[str, CorpCodeEntry] = {}
        self._loaded_at: float = 0.0
        self._lock = asyncio.Lock()

    @property
    def is_loaded(self) -> bool:
        return bool(self._entries)

    def _is_expired(self) -> bool:
        return (time.monotonic() - self._loaded_at) > _TTL_SECONDS

    async def _ensure_loaded(self, client: OpenDartClient) -> None:
        if self._entries and not self._is_expired():
            return
        async with self._lock:
            # double-check after acquiring lock
            if self._entries and not self._is_expired():
                return
            await self._load(client)

    async def _load(self, client: OpenDartClient) -> None:
        zip_bytes = await client.disclosure.download_corp_codes()
        entries: list[CorpCodeEntry] = []
        by_stock: dict[str, CorpCodeEntry] = {}
        by_name: dict[str, CorpCodeEntry] = {}

        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            xml_bytes = zf.read(zf.namelist()[0])

        root = ET.fromstring(xml_bytes)
        for item in root.iter("list"):
            corp_code = item.findtext("corp_code", "")
            corp_name = item.findtext("corp_name", "")
            raw_stock = item.findtext("stock_code", "")
            stock_code = raw_stock.strip() if raw_stock and raw_stock.strip() else None
            raw_modify = item.findtext("modify_date", "")
            modify_date = (
                raw_modify.strip() if raw_modify and raw_modify.strip() else None
            )

            name_lower = corp_name.lower()
            entry = CorpCodeEntry(
                corp_code=corp_code,
                corp_name=corp_name,
                corp_name_lower=name_lower,
                corp_name_chosung=extract_chosung(corp_name),
                stock_code=stock_code,
                modify_date=modify_date,
            )
            entries.append(entry)
            if stock_code:
                by_stock[stock_code] = entry
            by_name[name_lower] = entry

        self._entries = entries
        self._by_stock_code = by_stock
        self._by_name_lower = by_name
        self._loaded_at = time.monotonic()

    async def search(
        self,
        client: OpenDartClient,
        query: str,
        *,
        max_results: int = 10,
        listed_only: bool = False,
    ) -> list[CorpCodeEntry]:
        await self._ensure_loaded(client)

        query_stripped = query.strip()
        if not query_stripped:
            return []

        query_lower = query_stripped.lower()

        # Tier 0: Stock code exact match (O(1))
        if query_stripped in self._by_stock_code:
            entry = self._by_stock_code[query_stripped]
            return [entry]

        entries = self._entries
        if listed_only:
            entries = [e for e in entries if e.stock_code]

        # Tier 1-3: Exact / prefix / substring (single scan)
        exact: list[CorpCodeEntry] = []
        prefix: list[CorpCodeEntry] = []
        substring: list[CorpCodeEntry] = []

        for e in entries:
            name = e.corp_name_lower
            if name == query_lower:
                exact.append(e)
            elif name.startswith(query_lower):
                prefix.append(e)
            elif query_lower in name:
                substring.append(e)

        results = exact + prefix + substring

        # Tier 4: Chosung match (only when query contains chosung jamo)
        if len(results) < max_results and has_chosung(query_stripped):
            seen = {id(e) for e in results}
            query_normalized = normalize_mixed_query(query_stripped)
            chosung: list[CorpCodeEntry] = []
            for e in entries:
                if id(e) in seen:
                    continue
                if e.corp_name_chosung.startswith(query_normalized):
                    chosung.append(e)
                    if len(results) + len(chosung) >= max_results:
                        break
            results.extend(chosung)

        # Tier 5: Fuzzy match (only when results still < max_results and query >= 2 chars)
        if len(results) < max_results and len(query_stripped) >= 2:
            results = _apply_fuzzy(
                query_stripped,
                entries,
                results,
                max_results,
            )

        return results[:max_results]

    async def summary(self, client: OpenDartClient) -> dict:
        await self._ensure_loaded(client)
        total = len(self._entries)
        listed = len(self._by_stock_code)
        return {
            "total_count": total,
            "listed_count": listed,
            "unlisted_count": total - listed,
            "message": f"고유번호 목록 로드 완료: 전체 {total}개 (상장 {listed}개, 비상장 {total - listed}개)",
        }


def _apply_fuzzy(
    query: str,
    entries: list[CorpCodeEntry],
    existing: list[CorpCodeEntry],
    max_results: int,
) -> list[CorpCodeEntry]:
    """Append fuzzy-matched entries that are not already in *existing*."""
    from rapidfuzz import fuzz, process

    remaining = max_results - len(existing)
    if remaining <= 0:
        return existing

    seen = {id(e) for e in existing}

    # Build name→entry mapping for candidates not yet in results
    choices: dict[int, str] = {}
    entry_map: dict[int, CorpCodeEntry] = {}
    for e in entries:
        eid = id(e)
        if eid not in seen:
            choices[eid] = e.corp_name
            entry_map[eid] = e

    if not choices:
        return existing

    hits = process.extract(
        query,
        choices,
        scorer=fuzz.WRatio,
        score_cutoff=60,
        limit=remaining,
    )

    fuzzy_results: list[CorpCodeEntry] = []
    for _, _, key in hits:
        fuzzy_results.append(entry_map[key])

    return existing + fuzzy_results


_cache = CorpCodeCache()


def get_cache() -> CorpCodeCache:
    return _cache
