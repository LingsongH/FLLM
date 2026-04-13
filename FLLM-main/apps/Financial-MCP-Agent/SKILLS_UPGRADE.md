
# Financial-MCP-Agent Skills 增强版

这个版本在原项目基础上做了**加法**：

- 保留原有 `MCP client -> MCP server -> atomic tools` 链路
- 新增 `src/skills/` 目录，封装高层业务技能
- 四个分析 Agent 改为优先使用高层 skill，再按需回退到底层 raw tools
- `src/tools/mcp_config.py` 改为支持环境变量和相对路径，减少硬编码问题

## 新增目录

```text
src/skills/
├── __init__.py
├── README.md
├── base.py
├── contracts.py
├── company_profile_skill.py
├── fundamental_skill.py
├── technical_skill.py
├── valuation_skill.py
├── news_skill.py
└── registry.py
```

## 设计思路

- **MCP**：提供原子能力，如查财报、查K线、爬新闻
- **Skill**：组合多个原子工具，形成“公司画像 / 基本面采集 / 技术面采集 / 估值研究 / 新闻研究”高层能力
- **Agent**：理解任务、选择 skill、进行推理与总结

## 主要改动点

1. `company_profile_skill`：统一拉取公司基本信息、行业、最近交易日、历史分红
2. `fundamental_analysis_skill`：统一拉取盈利/成长/营运/偿债/现金流/杜邦/业绩披露
3. `technical_analysis_skill`：统一拉取最近交易日、建议分析窗、K线、复权因子
4. `valuation_analysis_skill`：统一拉取综合分析、盈利成长、分红和指数样本，给估值分析提供输入
5. `news_analysis_skill`：统一抓新闻，并复用服务器端已有的情感/风险打分链路
6. `registry.py`：为不同 Agent 生成 skill + raw tool 的混合工具包，并在运行时校验 skill 契约
7. `contracts.py`：统一声明 skill 所依赖的 MCP 工具，减少运行时隐性耦合

## 使用建议

在当前工作区结构中，推荐按以下路径放置：

- `apps/Financial-MCP-Agent`
- `services/a-share-mcp-is-just-i-need`

如果目录不一致，可在 `.env` 中设置：

```bash
A_SHARE_MCP_SERVER_DIR=/your/path/to/a-share-mcp-is-just-i-need
```
