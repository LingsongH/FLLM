# Skills Module

`src/skills` 用于把 MCP 原子工具组合成可复用的高层业务能力。

## Files

- `base.py`: 公共方法（调用、时间窗、报告片段渲染）
- `contracts.py`: 每个 skill 的工具契约定义
- `registry.py`: skill 注册、可用性筛选、agent 工具包生成
- `company_profile_skill.py`: 公司画像
- `fundamental_skill.py`: 基本面采集
- `technical_skill.py`: 技术面采集
- `valuation_skill.py`: 估值研究采集
- `news_skill.py`: 新闻研究采集

## Runtime behavior

1. 先从 MCP 服务加载原子工具。
2. `registry.py` 按 `contracts.py` 校验每个 skill 的必需工具。
3. 缺工具的 skill 自动跳过并输出 warning。
4. Agent 使用 `skills + raw fallback tools` 组合执行。

