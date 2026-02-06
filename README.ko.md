# opendart-fss-mcp

![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue)

[English](README.md)

금융감독원 전자공시시스템(DART) OpenAPI를 위한 MCP 서버입니다.

## OpenDART란?

[DART(전자공시시스템)](https://dart.fss.or.kr)는 금융감독원이 운영하는 기업공시 시스템으로, 모든 국내 법인의 사업보고서, 주요사항보고서, 지분공시 등이 제출됩니다. 미국의 SEC EDGAR에 해당하는 시스템입니다.

[OpenDART](https://opendart.fss.or.kr)는 이 데이터를 프로그래밍 방식으로 접근할 수 있는 공개 API를 제공합니다.

## 주요 기능

- DART API 6개 카테고리를 아우르는 **84개 도구** — 공시검색, 재무제표, 정기보고서, 지분공시, 주요사항, 증권신고서
- **stdio** 및 **HTTP (Streamable HTTP)** MCP 서버 모드 지원
- **Claude Desktop**, **Claude Code** 등 MCP 호환 클라이언트와 연동
- [FastMCP](https://github.com/jlowin/fastmcp) 및 [opendart-fss](https://github.com/hypn4/opendart-fss-python) SDK 기반

## 사전 요구사항

- **Python 3.14+**
- **[uv](https://docs.astral.sh/uv/)** (권장 패키지 매니저)
- **OpenDART API 키** — [opendart.fss.or.kr](https://opendart.fss.or.kr)에서 무료 발급

## 설치

```bash
uv pip install opendart-fss-mcp
```

또는 소스에서 설치:

```bash
git clone https://github.com/hypn4/opendart-fss-mcp.git
cd opendart-fss-mcp
uv sync
```

## 설정

`.env.example`을 `.env`로 복사한 후 값을 설정합니다:

```bash
cp .env.example .env
```

| 변수 | 설명 | 기본값 |
|---|---|---|
| `OPENDART_API_KEY` | OpenDART API 키 (**필수**) | — |
| `OPENDART_MCP_TRANSPORT` | 전송 프로토콜: `stdio` \| `http` | `stdio` |
| `OPENDART_MCP_HOST` | HTTP 바인딩 주소 | `127.0.0.1` |
| `OPENDART_MCP_PORT` | HTTP 포트 | `8000` |
| `OPENDART_MCP_LOG_LEVEL` | 로그 레벨: `DEBUG` \| `INFO` \| `WARNING` \| `ERROR` \| `CRITICAL` | `INFO` |

## 사용법

### Claude Desktop

Claude Desktop 설정 파일(`claude_desktop_config.json`)에 추가합니다:

```json
{
  "mcpServers": {
    "opendart": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/path/to/opendart-fss-mcp",
        "opendart-mcp"
      ],
      "env": {
        "OPENDART_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add opendart -- uv run --directory /path/to/opendart-fss-mcp opendart-mcp
```

### CLI

```bash
# stdio 모드 (기본값)
opendart-mcp

# HTTP 모드
opendart-mcp --transport http --host 127.0.0.1 --port 8000
```

### FastMCP

```bash
fastmcp run src/opendart_fss_mcp/server.py:mcp
```

## 제공 도구

6개 카테고리, 총 84개 도구:

| 카테고리 | 접두사 | 도구 수 | 설명 |
|---|---|---|---|
| 공시정보 | `disclosure_` | 5 | 기업 개황, 공시 검색, 문서 뷰어 |
| 재무정보 | `financial_` | 7 | 재무제표 (단일/다중 계정, XBRL) |
| 정기보고서 | `report_` | 28 | 정기보고서 주요항목 (보수, 자본, 임원 등) |
| 지분공시 | `shareholder_` | 2 | 대량보유 및 임원 지분 |
| 주요사항 | `event_` | 36 | M&A, 자본변동, 주식이벤트, 소송 등 |
| 증권신고서 | `registration_` | 6 | 증권신고서 세부정보 |

## 개발

```bash
# 개발 의존성 설치
uv sync

# 테스트 실행
uv run pytest

# 린트 & 포맷
uv run ruff check .
uv run ruff format .

# 타입 체크
uv run pyright
```

## 라이선스

MIT

## 링크

- [OpenDART](https://opendart.fss.or.kr) — OpenDART API 공식 포털
- [DART](https://dart.fss.or.kr) — 전자공시시스템
- [opendart-fss](https://github.com/hypn4/opendart-fss-python) — OpenDART API Python SDK
