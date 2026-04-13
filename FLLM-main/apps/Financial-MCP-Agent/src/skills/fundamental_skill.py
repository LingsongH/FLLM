
from __future__ import annotations

from langchain_core.tools import tool

from .base import build_tool_map, call_tool_async, render_sections, resolve_reporting_period


def build_fundamental_skill(mcp_tools):
    tool_map = build_tool_map(mcp_tools)

    @tool("fundamental_analysis_skill")
    async def fundamental_analysis_skill(stock_code: str, year: str = "", quarter: int = 0) -> str:
        """执行高层基本面采集。输入股票代码，可选财报年份和季度；未提供时自动使用最近已结束季度。输出盈利、成长、营运、资产负债、现金流、杜邦分析和业绩披露组合结果。"""
        actual_year, actual_quarter = resolve_reporting_period(year or None, quarter or None)
        period = {"code": stock_code, "year": actual_year, "quarter": actual_quarter}

        profit = await call_tool_async(tool_map, "get_profit_data", period)
        growth = await call_tool_async(tool_map, "get_growth_data", period)
        operation = await call_tool_async(tool_map, "get_operation_data", period)
        balance = await call_tool_async(tool_map, "get_balance_data", period)
        cash_flow = await call_tool_async(tool_map, "get_cash_flow_data", period)
        dupont = await call_tool_async(tool_map, "get_dupont_data", period)

        date_end = f"{actual_year}-12-31" if int(actual_quarter) == 4 else f"{actual_year}-{int(actual_quarter) * 3:02d}-28"
        date_start = f"{int(actual_year) - 1}-01-01"
        express = await call_tool_async(tool_map, "get_performance_express_report", {"code": stock_code, "start_date": date_start, "end_date": date_end})
        forecast = await call_tool_async(tool_map, "get_forecast_report", {"code": stock_code, "start_date": date_start, "end_date": date_end})

        return render_sections(
            f"{stock_code} 基本面技能输出（{actual_year}Q{actual_quarter}）",
            [
                ("盈利能力", profit),
                ("成长能力", growth),
                ("营运能力", operation),
                ("资产负债与偿债", balance),
                ("现金流", cash_flow),
                ("杜邦分析", dupont),
                ("业绩快报", express),
                ("业绩预告", forecast),
            ],
        )

    return fundamental_analysis_skill
