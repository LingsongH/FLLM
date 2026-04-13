
from __future__ import annotations

from langchain_core.tools import tool

from .base import build_tool_map, call_tool_async, render_sections


def build_news_skill(mcp_tools):
    tool_map = build_tool_map(mcp_tools)

    @tool("news_analysis_skill")
    async def news_analysis_skill(company_name: str = "", stock_code: str = "", top_k: int = 8) -> str:
        """执行高层新闻研究。输入公司名和可选股票代码，优先按公司名抓取新闻。输出最近交易日以及包含新闻正文、情感分析和风险分析的整合结果。"""
        latest_date = await call_tool_async(tool_map, "get_latest_trading_date", {})
        query = company_name or stock_code
        news = await call_tool_async(tool_map, "crawl_news", {"query": query, "top_k": top_k})
        return render_sections(
            f"{query or stock_code} 新闻技能输出",
            [
                ("最近交易日", latest_date),
                ("新闻抓取与情感/风险结果", news),
            ],
        )

    return news_analysis_skill
