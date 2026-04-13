from __future__ import annotations

from datetime import datetime

from langchain_core.tools import tool

from .base import build_tool_map, call_tool_async, render_sections


def build_company_profile_skill(mcp_tools):
    tool_map = build_tool_map(mcp_tools)

    @tool("company_profile_skill")
    async def company_profile_skill(stock_code: str, company_name: str = "") -> str:
        """获取公司画像。适合在任何分析开始前优先使用。输入股票代码（如 sh.600519）和可选公司名，输出最近交易日、基础信息、行业分类和近期分红信息的组合结果。"""
        latest_date = await call_tool_async(tool_map, "get_latest_trading_date", {})
        basic_info = await call_tool_async(tool_map, "get_stock_basic_info", {"code": stock_code})
        industry_info = await call_tool_async(tool_map, "get_stock_industry", {"code": stock_code})

        current_year = datetime.now().year
        dividend_sections = []
        for year in [str(current_year - 1), str(current_year - 2)]:
            dividend_result = await call_tool_async(
                tool_map,
                "get_dividend_data",
                {"code": stock_code, "year": year, "year_type": "report"},
            )
            dividend_sections.append(f"### {year}年分红\n{dividend_result}")

        title = f"{company_name or stock_code} 公司画像"
        return render_sections(
            title,
            [
                ("最近交易日", latest_date),
                ("股票基本信息", basic_info),
                ("行业分类", industry_info),
                ("历史分红", "\n\n".join(dividend_sections).strip()),
            ],
        )

    return company_profile_skill
