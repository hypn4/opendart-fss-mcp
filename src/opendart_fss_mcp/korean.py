"""Korean text utilities: chosung extraction and query helpers."""

from __future__ import annotations

# 19 Korean initial consonants (chosung) in Unicode order
_CHOSUNG = (
    "ㄱ",
    "ㄲ",
    "ㄴ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
)

# Set of all chosung jamo for fast lookup
_CHOSUNG_SET = frozenset(_CHOSUNG)

_HANGUL_BASE = 0xAC00
_HANGUL_END = 0xD7A3
_JUNGSUNG_COUNT = 21
_JONGSUNG_COUNT = 28


def extract_chosung(text: str) -> str:
    """Extract initial consonants from Korean syllables; lowercase non-Hangul.

    Examples:
        >>> extract_chosung("삼성전자")
        'ㅅㅅㅈㅈ'
        >>> extract_chosung("삼성SDI")
        'ㅅㅅsdi'
        >>> extract_chosung("LG전자")
        'lgㅈㅈ'
    """
    result: list[str] = []
    for ch in text:
        code = ord(ch)
        if _HANGUL_BASE <= code <= _HANGUL_END:
            index = (code - _HANGUL_BASE) // (_JUNGSUNG_COUNT * _JONGSUNG_COUNT)
            result.append(_CHOSUNG[index])
        else:
            result.append(ch.lower())
    return "".join(result)


def has_chosung(query: str) -> bool:
    """Return True if *query* contains any chosung jamo (ㄱ-ㅎ)."""
    return any(ch in _CHOSUNG_SET for ch in query)


def is_pure_chosung(query: str) -> bool:
    """Return True if *query* consists entirely of chosung jamo."""
    return bool(query) and all(ch in _CHOSUNG_SET for ch in query)


def normalize_mixed_query(query: str) -> str:
    """Normalize a mixed chosung/non-chosung query for matching.

    Chosung characters are kept as-is; non-chosung characters are lowered.

    Examples:
        >>> normalize_mixed_query("ㅅㅅSDI")
        'ㅅㅅsdi'
    """
    return "".join(ch if ch in _CHOSUNG_SET else ch.lower() for ch in query)
