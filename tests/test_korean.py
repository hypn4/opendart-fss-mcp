"""Tests for korean text utilities."""

from __future__ import annotations

from opendart_fss_mcp.korean import (
    extract_chosung,
    has_chosung,
    is_pure_chosung,
    normalize_mixed_query,
)


# -- extract_chosung -----------------------------------------------------------


def test_extract_chosung_hangul_only() -> None:
    assert extract_chosung("삼성전자") == "ㅅㅅㅈㅈ"


def test_extract_chosung_mixed() -> None:
    assert extract_chosung("삼성SDI") == "ㅅㅅsdi"


def test_extract_chosung_english_only() -> None:
    assert extract_chosung("LG") == "lg"


def test_extract_chosung_mixed_prefix() -> None:
    assert extract_chosung("LG전자") == "lgㅈㅈ"


def test_extract_chosung_empty() -> None:
    assert extract_chosung("") == ""


# -- has_chosung ---------------------------------------------------------------


def test_has_chosung_true() -> None:
    assert has_chosung("ㅅㅅㅈㅈ") is True


def test_has_chosung_mixed() -> None:
    assert has_chosung("ㅅㅅSDI") is True


def test_has_chosung_no_chosung() -> None:
    assert has_chosung("삼성전자") is False


def test_has_chosung_empty() -> None:
    assert has_chosung("") is False


# -- is_pure_chosung -----------------------------------------------------------


def test_is_pure_chosung_true() -> None:
    assert is_pure_chosung("ㅅㅅㅈㅈ") is True


def test_is_pure_chosung_mixed() -> None:
    assert is_pure_chosung("ㅅㅅSDI") is False


def test_is_pure_chosung_empty() -> None:
    assert is_pure_chosung("") is False


# -- normalize_mixed_query -----------------------------------------------------


def test_normalize_mixed_query() -> None:
    assert normalize_mixed_query("ㅅㅅSDI") == "ㅅㅅsdi"


def test_normalize_mixed_query_pure_chosung() -> None:
    assert normalize_mixed_query("ㅅㅅㅈㅈ") == "ㅅㅅㅈㅈ"


def test_normalize_mixed_query_no_chosung() -> None:
    assert normalize_mixed_query("Samsung") == "samsung"
