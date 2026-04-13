from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class SkillContract:
    name: str
    description: str
    required_tools: List[str]
    optional_tools: List[str]


SKILL_CONTRACTS: Dict[str, SkillContract] = {
    "company_profile_skill": SkillContract(
        name="company_profile_skill",
        description="公司画像聚合：最近交易日、基础信息、行业、分红。",
        required_tools=["get_latest_trading_date", "get_stock_basic_info", "get_stock_industry", "get_dividend_data"],
        optional_tools=[],
    ),
    "fundamental_analysis_skill": SkillContract(
        name="fundamental_analysis_skill",
        description="基本面聚合：盈利、成长、运营、资产负债、现金流、杜邦、业绩披露。",
        required_tools=[
            "get_profit_data",
            "get_growth_data",
            "get_operation_data",
            "get_balance_data",
            "get_cash_flow_data",
            "get_dupont_data",
            "get_performance_express_report",
            "get_forecast_report",
        ],
        optional_tools=[],
    ),
    "technical_analysis_skill": SkillContract(
        name="technical_analysis_skill",
        description="技术面聚合：最近交易日、时间窗、K线、复权因子。",
        required_tools=["get_latest_trading_date", "get_market_analysis_timeframe", "get_historical_k_data", "get_adjust_factor_data"],
        optional_tools=[],
    ),
    "valuation_analysis_skill": SkillContract(
        name="valuation_analysis_skill",
        description="估值研究聚合：公司画像、综合分析、盈利成长、分红与指数样本。",
        required_tools=["get_stock_basic_info", "get_stock_industry", "get_stock_analysis", "get_profit_data", "get_growth_data", "get_dividend_data"],
        optional_tools=["get_hs300_stocks", "get_zz500_stocks", "get_sz50_stocks"],
    ),
    "news_analysis_skill": SkillContract(
        name="news_analysis_skill",
        description="新闻研究聚合：最近交易日、新闻抓取、情感与风险结果。",
        required_tools=["get_latest_trading_date", "crawl_news"],
        optional_tools=[],
    ),
}

