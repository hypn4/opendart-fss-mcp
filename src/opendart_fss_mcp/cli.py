"""OpenDART MCP Server CLI."""

from __future__ import annotations

from enum import StrEnum

import typer
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer(
    name="opendart-mcp",
    help="OpenDART FSS MCP Server",
    no_args_is_help=False,
    invoke_without_command=True,
)


class Transport(StrEnum):
    STDIO = "stdio"
    HTTP = "http"


@app.callback()
def serve(
    transport: Transport = typer.Option(
        Transport.STDIO,
        envvar="OPENDART_MCP_TRANSPORT",
        help="Transport protocol: stdio | http",
    ),
    host: str = typer.Option(
        "127.0.0.1", envvar="OPENDART_MCP_HOST", help="HTTP bind address"
    ),
    port: int = typer.Option(8000, envvar="OPENDART_MCP_PORT", help="HTTP port"),
    api_key: str | None = typer.Option(
        None, envvar="OPENDART_API_KEY", help="OpenDART API key"
    ),
    log_level: str = typer.Option(
        "INFO", envvar="OPENDART_MCP_LOG_LEVEL", help="Log level"
    ),
) -> None:
    """OpenDART MCP 서버를 시작합니다."""
    from opendart_fss_mcp import deps
    from opendart_fss_mcp.server import mcp

    deps.configure(api_key)

    kwargs: dict = {"transport": transport.value, "log_level": log_level}
    if transport == Transport.HTTP:
        kwargs["host"] = host
        kwargs["port"] = port

    mcp.run(**kwargs)
