
"""MCP服务器配置模块 - 支持环境变量覆盖和相对路径回退。"""

from __future__ import annotations

import os
from pathlib import Path


def _resolve_server_dir() -> str:
    env_dir = os.getenv("A_SHARE_MCP_SERVER_DIR")
    if env_dir:
        return env_dir

    current = Path(__file__).resolve()
    candidates = [
        current.parents[4] / "services" / "a-share-mcp-is-just-i-need",  # 新目录结构
        current.parents[4] / "a-share-mcp-is-just-i-need",  # 兼容旧目录结构
        current.parents[3] / "a-share-mcp-is-just-i-need",  # 与 Financial-MCP-Agent 同级
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return str(candidates[0])


SERVER_CONFIGS = {
    "a_share_mcp_v2": {
        "command": os.getenv("A_SHARE_MCP_COMMAND", "uv"),
        "args": [
            "run",
            "--directory",
            _resolve_server_dir(),
            "python",
            os.getenv("A_SHARE_MCP_ENTRY", "mcp_server.py"),
        ],
        "transport": "stdio",
    }
}
