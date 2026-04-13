from __future__ import annotations

import logging
from typing import Any, Iterable, List

from .company_profile_skill import build_company_profile_skill
from .contracts import SKILL_CONTRACTS
from .fundamental_skill import build_fundamental_skill
from .news_skill import build_news_skill
from .technical_skill import build_technical_skill
from .valuation_skill import build_valuation_skill

logger = logging.getLogger(__name__)

SKILL_NAME_MAP = {
    "company_profile_skill": build_company_profile_skill,
    "fundamental_analysis_skill": build_fundamental_skill,
    "technical_analysis_skill": build_technical_skill,
    "valuation_analysis_skill": build_valuation_skill,
    "news_analysis_skill": build_news_skill,
}

AGENT_SKILLS = {
    "fundamental": ["company_profile_skill", "fundamental_analysis_skill"],
    "technical": ["company_profile_skill", "technical_analysis_skill"],
    "value": ["company_profile_skill", "valuation_analysis_skill"],
    "news": ["news_analysis_skill"],
}

RAW_TOOL_ALLOWLIST = {
    "fundamental": [
        "get_latest_trading_date",
        "get_stock_basic_info",
        "get_stock_industry",
        "get_profit_data",
        "get_operation_data",
        "get_growth_data",
        "get_balance_data",
        "get_cash_flow_data",
        "get_dupont_data",
        "get_dividend_data",
        "get_performance_express_report",
        "get_forecast_report",
        "get_stock_analysis",
    ],
    "technical": [
        "get_latest_trading_date",
        "get_market_analysis_timeframe",
        "get_stock_basic_info",
        "get_historical_k_data",
        "get_adjust_factor_data",
        "get_stock_analysis",
    ],
    "value": [
        "get_latest_trading_date",
        "get_stock_basic_info",
        "get_stock_industry",
        "get_profit_data",
        "get_growth_data",
        "get_dividend_data",
        "get_stock_analysis",
        "get_hs300_stocks",
        "get_zz500_stocks",
        "get_sz50_stocks",
    ],
    "news": [
        "get_latest_trading_date",
        "crawl_news",
    ],
}


def filter_tools_by_name(tools: Iterable[Any], allowed_names: Iterable[str]) -> List[Any]:
    allowed = set(allowed_names)
    return [tool for tool in tools if getattr(tool, "name", None) in allowed]


def _tool_name_set(mcp_tools: Iterable[Any]) -> set[str]:
    return {getattr(tool, "name", "") for tool in mcp_tools}


def _missing_required_tools(skill_name: str, mcp_tool_names: set[str]) -> List[str]:
    contract = SKILL_CONTRACTS.get(skill_name)
    if not contract:
        return []
    return [tool_name for tool_name in contract.required_tools if tool_name not in mcp_tool_names]


def _available_skill_builders(mcp_tools: Iterable[Any]) -> dict[str, Any]:
    tool_names = _tool_name_set(mcp_tools)
    available: dict[str, Any] = {}
    for skill_name, builder in SKILL_NAME_MAP.items():
        missing = _missing_required_tools(skill_name, tool_names)
        if missing:
            logger.warning("Skip skill %s due to missing MCP tools: %s", skill_name, missing)
            continue
        available[skill_name] = builder
    return available


def build_skill_tools(mcp_tools: Iterable[Any]) -> List[Any]:
    return [builder(mcp_tools) for builder in _available_skill_builders(mcp_tools).values()]


def get_agent_tool_bundle(agent_type: str, mcp_tools: Iterable[Any]) -> List[Any]:
    skill_tools = build_skill_tools(mcp_tools)
    skill_map = {tool.name: tool for tool in skill_tools}
    selected_skills = [skill_map[name] for name in AGENT_SKILLS.get(agent_type, []) if name in skill_map]
    raw_tools = filter_tools_by_name(mcp_tools, RAW_TOOL_ALLOWLIST.get(agent_type, []))
    return selected_skills + raw_tools


def describe_agent_tool_bundle(agent_type: str, mcp_tools: Iterable[Any]) -> dict:
    selected_skill_names = AGENT_SKILLS.get(agent_type, [])
    tool_names = _tool_name_set(mcp_tools)
    unavailable_skills = {
        skill_name: _missing_required_tools(skill_name, tool_names)
        for skill_name in selected_skill_names
        if _missing_required_tools(skill_name, tool_names)
    }

    bundle = get_agent_tool_bundle(agent_type, mcp_tools)
    skill_names = [tool.name for tool in bundle if tool.name in selected_skill_names]
    raw_names = [tool.name for tool in bundle if tool.name not in skill_names]
    return {
        "agent_type": agent_type,
        "skills": skill_names,
        "unavailable_skills": unavailable_skills,
        "raw_tools": raw_names,
        "bundle_size": len(bundle),
    }

