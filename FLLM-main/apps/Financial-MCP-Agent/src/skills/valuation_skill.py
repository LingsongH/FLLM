
from __future__ import annotations

from datetime import datetime

from langchain_core.tools import tool

from .base import build_tool_map, call_tool_async, render_sections, resolve_reporting_period


def build_valuation_skill(mcp_tools):
    tool_map = build_tool_map(mcp_tools)

    @tool("valuation_analysis_skill")
    async def valuation_analysis_skill(stock_code: str, year: str = "", quarter: int = 0, benchmark_index: str = "hs300") -> str:
        """执行高层估值研究采集。输入股票代码，可选财报年份、季度和对标指数。输出公司画像、综合数据分析、分红、盈利和成长数据，用于支持估值判断。"""
        actual_year, actual_quarter = resolve_reporting_period(year or None, quarter or None)
        basic_info = await call_tool_async(tool_map, "get_stock_basic_info", {"code": stock_code})
        industry_info = await call_tool_async(tool_map, "get_stock_industry", {"code": stock_code})
        analysis_report = await call_tool_async(tool_map, "get_stock_analysis", {"code": stock_code, "analysis_type": "comprehensive"})
        profit = await call_tool_async(tool_map, "get_profit_data", {"code": stock_code, "year": actual_year, "quarter": actual_quarter})
        growth = await call_tool_async(tool_map, "get_growth_data", {"code": stock_code, "year": actual_year, "quarter": actual_quarter})
        dividend = await call_tool_async(tool_map, "get_dividend_data", {"code": stock_code, "year": str(datetime.now().year - 1), "year_type": "report"})

        benchmark_tool = {
            "hs300": "get_hs300_stocks",
            "zz500": "get_zz500_stocks",
            "sz50": "get_sz50_stocks",
        }.get(benchmark_index.lower(), "get_hs300_stocks")
        benchmark = await call_tool_async(tool_map, benchmark_tool, {})

        return render_sections(
            f"{stock_code} 估值研究技能输出",
            [
                ("公司基本信息", basic_info),
                ("行业分类", industry_info),
                ("综合数据分析", analysis_report),
                ("盈利能力", profit),
                ("成长能力", growth),
                ("分红信息", dividend),
                ("对标指数样本", benchmark),
            ],
        )

    return valuation_analysis_skill
