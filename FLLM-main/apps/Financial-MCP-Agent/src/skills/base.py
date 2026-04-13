from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List, Mapping


class SkillToolError(RuntimeError):
    """Raised when a required underlying MCP tool is missing."""


def build_tool_map(mcp_tools: Iterable[Any]) -> Dict[str, Any]:
    return {tool.name: tool for tool in mcp_tools if hasattr(tool, "name")}


async def call_tool_async(tool_map: Mapping[str, Any], tool_name: str, args: Dict[str, Any]) -> str:
    tool = tool_map.get(tool_name)
    if tool is None:
        raise SkillToolError(f"Missing required MCP tool: {tool_name}")

    if hasattr(tool, "ainvoke"):
        result = await tool.ainvoke(args)
    elif hasattr(tool, "invoke"):
        result = tool.invoke(args)
    elif callable(tool):
        result = tool(**args)
    else:
        raise SkillToolError(f"Tool {tool_name} is not invokable")

    if result is None:
        return ""
    return str(result)


def render_sections(title: str, sections: List[tuple[str, str]]) -> str:
    lines: List[str] = [f"# {title}"]
    for section_title, content in sections:
        content = (content or "").strip()
        if not content:
            continue
        lines.append(f"\n## {section_title}\n{content}")
    return "\n".join(lines).strip()


def resolve_reporting_period(year: str | None = None, quarter: int | None = None) -> tuple[str, int]:
    now = datetime.now()
    if year and quarter:
        return str(year), int(quarter)

    current_quarter = (now.month - 1) // 3 + 1
    if current_quarter == 1:
        return str(now.year - 1), 4
    return str(now.year), current_quarter - 1


def resolve_date_window(latest_trading_date: str | None, lookback_days: int) -> tuple[str, str]:
    end_dt = datetime.strptime(latest_trading_date, "%Y-%m-%d") if latest_trading_date else datetime.now()
    start_dt = end_dt - timedelta(days=max(lookback_days, 30))
    return start_dt.strftime("%Y-%m-%d"), end_dt.strftime("%Y-%m-%d")


def choose_period_name(lookback_days: int) -> str:
    if lookback_days <= 70:
        return "recent"
    if lookback_days <= 120:
        return "quarter"
    if lookback_days <= 220:
        return "half_year"
    return "year"
