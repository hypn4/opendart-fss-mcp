"""Corp code cache: ZIP download, XML parsing, in-memory cache, and search."""

from __future__ import annotations

import asyncio
import io
import time
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass

from opendart_fss import OpenDartClient

_TTL_SECONDS = 24 * 60 * 60  # 24 hours


@dataclass(slots=True)
class CorpCodeEntry:
    corp_code: str
    corp_name: str
    corp_name_lower: str  # pre-lowered for search
    stock_code: str | None
    modify_date: str | None


class CorpCodeCache:
    """Lazy-loaded, TTL-based in-memory cache for DART corp codes."""

    def __init__(self) -> None:
        self._entries: list[CorpCodeEntry] = []
        self._by_stock_code: dict[str, CorpCodeEntry] = {}
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

        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            xml_bytes = zf.read(zf.namelist()[0])

        root = ET.fromstring(xml_bytes)
        for item in root.iter("list"):
            corp_code = item.findtext("corp_code", "")
            corp_name = item.findtext("corp_name", "")
            raw_stock = item.findtext("stock_code", "")
            stock_code = raw_stock.strip() if raw_stock and raw_stock.strip() else None
            raw_modify = item.findtext("modify_date", "")
            modify_date = raw_modify.strip() if raw_modify and raw_modify.strip() else None

            entry = CorpCodeEntry(
                corp_code=corp_code,
                corp_name=corp_name,
                corp_name_lower=corp_name.lower(),
                stock_code=stock_code,
                modify_date=modify_date,
            )
            entries.append(entry)
            if stock_code:
                by_stock[stock_code] = entry

        self._entries = entries
        self._by_stock_code = by_stock
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

        # 1. Stock code exact match
        if query_stripped in self._by_stock_code:
            entry = self._by_stock_code[query_stripped]
            return [entry]

        entries = self._entries
        if listed_only:
            entries = [e for e in entries if e.stock_code]

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


_cache = CorpCodeCache()


def get_cache() -> CorpCodeCache:
    return _cache
