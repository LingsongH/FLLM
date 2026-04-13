
from __future__ import annotations

from langchain_core.tools import tool

from .base import (
    build_tool_map,
    call_tool_async,
    choose_period_name,
    render_sections,
    resolve_date_window,
)


def build_technical_skill(mcp_tools):
    tool_map = build_tool_map(mcp_tools)

    @tool("technical_analysis_skill")
    async def technical_analysis_skill(stock_code: str, lookback_days: int = 180, frequency: str = "d", adjust_flag: str = "3") -> str:
        """执行高层技术面采集。输入股票代码，可选回看天数、频率和复权方式。输出最近交易日、建议分析时间窗、K线数据和复权因子。"""
        latest_date = await call_tool_async(tool_map, "get_latest_trading_date", {})
        start_date, end_date = resolve_date_window(latest_date.strip(), lookback_days)
        timeframe = await call_tool_async(tool_map, "get_market_analysis_timeframe", {"period": choose_period_name(lookback_days)})
        k_data = await call_tool_async(
            tool_map,
            "get_historical_k_data",
            {
                "code": stock_code,
                "start_date": start_date,
                "end_date": end_date,
                "frequency": frequency,
                "adjust_flag": adjust_flag,
            },
        )
        adjust_factor = await call_tool_async(tool_map, "get_adjust_factor_data", {"code": stock_code, "start_date": start_date, "end_date": end_date})

        return render_sections(
            f"{stock_code} 技术面技能输出",
            [
                ("最近交易日", latest_date),
                ("建议分析时间窗", timeframe),
                ("历史K线数据", k_data),
                ("复权因子", adjust_factor),
            ],
        )

    return technical_analysis_skill
