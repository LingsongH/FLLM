# Skills System Design

本文描述 `apps/Financial-MCP-Agent/src/skills` 的能力边界与实现约束。

## 1. 核心原则

1. Skill 是业务语义能力，不是原子查询。
2. Skill 必须可复用，输入输出稳定。
3. Skill 必须声明契约：依赖哪些 MCP 工具。
4. Agent 应先用 skill 做首轮采集，再用 raw tool 补齐。

## 2. 文件说明

- `base.py`: 通用工具调用与时间窗计算函数
- `contracts.py`: skill 契约（required/optional tools）
- `registry.py`: skill 注册、可用性筛选、agent 工具包组装
- `*_skill.py`: 各业务技能实现

## 3. Skill 清单

| Skill | 作用 | 必需 MCP 工具 |
|---|---|---|
| `company_profile_skill` | 公司画像聚合 | `get_latest_trading_date`, `get_stock_basic_info`, `get_stock_industry`, `get_dividend_data` |
| `fundamental_analysis_skill` | 基本面数据聚合 | `get_profit_data`, `get_growth_data`, `get_operation_data`, `get_balance_data`, `get_cash_flow_data`, `get_dupont_data`, `get_performance_express_report`, `get_forecast_report` |
| `technical_analysis_skill` | 技术面数据聚合 | `get_latest_trading_date`, `get_market_analysis_timeframe`, `get_historical_k_data`, `get_adjust_factor_data` |
| `valuation_analysis_skill` | 估值研究数据聚合 | `get_stock_basic_info`, `get_stock_industry`, `get_stock_analysis`, `get_profit_data`, `get_growth_data`, `get_dividend_data` |
| `news_analysis_skill` | 新闻研究聚合 | `get_latest_trading_date`, `crawl_news` |

## 4. Agent 绑定策略

- `fundamental`: `company_profile_skill` + `fundamental_analysis_skill`
- `technical`: `company_profile_skill` + `technical_analysis_skill`
- `value`: `company_profile_skill` + `valuation_analysis_skill`
- `news`: `news_analysis_skill`

## 5. 运行时可用性策略

`registry.py` 的处理逻辑：
1. 收集 MCP 工具名集合
2. 对每个 skill 检查契约中的必需工具
3. 必需工具不完整时跳过 skill 并记录 warning
4. 构建 “可用 skills + raw allowlist” 工具包

这样即使底层服务能力不完整，系统也能降级运行，不会因为单个 skill 初始化失败而整体中断。
