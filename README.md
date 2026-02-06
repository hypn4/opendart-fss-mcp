# opendart-fss-mcp

![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue)

[한국어](README.ko.md)

MCP server for Korea's DART (Financial Supervisory Service) corporate disclosure API.

## What is OpenDART?

[DART (Data Analysis, Retrieval and Transfer System)](https://dart.fss.or.kr) is Korea's equivalent of the SEC's EDGAR system. It is the official electronic disclosure system operated by the Financial Supervisory Service (FSS) where all Korean corporations submit their financial reports, major event disclosures, and shareholding information.

[OpenDART](https://opendart.fss.or.kr) provides a public API to access this data programmatically.

## Features

- **84 tools** covering 6 DART API categories — disclosure search, financial statements, periodic reports, shareholding, major events, and securities registration
- Runs as a **stdio** or **HTTP (Streamable HTTP)** MCP server
- Works with **Claude Desktop**, **Claude Code**, and any MCP-compatible client
- Built on [FastMCP](https://github.com/jlowin/fastmcp) and [opendart-fss](https://github.com/hypn4/opendart-fss-python) SDK

## Prerequisites

- **Python 3.14+**
- **[uv](https://docs.astral.sh/uv/)** (recommended package manager)
- **OpenDART API Key** — get one free at [opendart.fss.or.kr](https://opendart.fss.or.kr)

## Installation

```bash
uv pip install opendart-fss-mcp
```

Or install from source:

```bash
git clone https://github.com/hypn4/opendart-fss-mcp.git
cd opendart-fss-mcp
uv sync
```

## Configuration

Copy `.env.example` to `.env` and set your values:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|---|---|---|
| `OPENDART_API_KEY` | OpenDART API key (**required**) | — |
| `OPENDART_MCP_TRANSPORT` | Transport protocol: `stdio` \| `http` | `stdio` |
| `OPENDART_MCP_HOST` | HTTP bind address | `127.0.0.1` |
| `OPENDART_MCP_PORT` | HTTP port | `8000` |
| `OPENDART_MCP_LOG_LEVEL` | Log level: `DEBUG` \| `INFO` \| `WARNING` \| `ERROR` \| `CRITICAL` | `INFO` |

## Usage

### Claude Desktop

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

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
# stdio mode (default)
opendart-mcp

# HTTP mode
opendart-mcp --transport http --host 127.0.0.1 --port 8000
```

### FastMCP

```bash
fastmcp run src/opendart_fss_mcp/server.py:mcp
```

## Available Tools

84 tools organized into 6 categories:

| Category | Prefix | Tools | Description |
|---|---|---|---|
| Disclosure | `disclosure_` | 5 | Company search, disclosure list, document viewer |
| Financial | `financial_` | 7 | Financial statements (single/multi account, XBRL) |
| Report | `report_` | 28 | Periodic report key items (compensation, capital, directors, etc.) |
| Shareholding | `shareholder_` | 2 | Major shareholder and executive holdings |
| Major Events | `event_` | 36 | M&A, capital changes, stock events, lawsuits, and more |
| Registration | `registration_` | 6 | Securities registration statement details |

## Development

```bash
# Install dev dependencies
uv sync

# Run tests
uv run pytest

# Lint & format
uv run ruff check .
uv run ruff format .

# Type check
uv run pyright
```

## License

MIT

## Links

- [OpenDART](https://opendart.fss.or.kr) — Official OpenDART API portal
- [DART](https://dart.fss.or.kr) — Electronic Disclosure System
- [opendart-fss](https://github.com/hypn4/opendart-fss-python) — Python SDK for OpenDART API
