
# Financial-MCP-Agent Skills


1. `company_profile_skill`：统一拉取公司基本信息、行业、最近交易日、历史分红
2. `fundamental_analysis_skill`：统一拉取盈利/成长/营运/偿债/现金流/杜邦/业绩披露
3. `technical_analysis_skill`：统一拉取最近交易日、建议分析窗、K线、复权因子
4. `valuation_analysis_skill`：统一拉取综合分析、盈利成长、分红和指数样本，给估值分析提供输入
5. `news_analysis_skill`：统一抓新闻，并复用服务器端已有的情感/风险打分链路
6. `registry.py`：为不同 Agent 生成 skill + raw tool 的混合工具包，并在运行时校验 skill 契约
7. `contracts.py`：统一声明 skill 所依赖的 MCP 工具，减少运行时隐性耦合

## 使用建议

在当前工作区结构中，按以下路径放置：

- `apps/Financial-MCP-Agent`
- `services/a-share-mcp-is-just-i-need`

如果目录不一致，可在 `.env` 中设置：

```bash
A_SHARE_MCP_SERVER_DIR=/your/path/to/a-share-mcp-is-just-i-need
```
