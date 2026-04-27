# Finance Multi-Agent Research Workspace

一个以 A 股投研为核心的多模块金融智能体工作区，包含：
- 多智能体投研应用（`apps/Financial-MCP-Agent`）
- A 股 MCP 服务（`services/a-share-mcp-is-just-i-need`）
- 新闻情感/风险数据与训练流水线（`data` + `pipelines`）

## 1. 设计目标

本项目采用“原子工具 -> 业务技能 -> 分析智能体 -> 汇总报告”的分层架构，目标是：
1. 把数据获取能力与推理能力解耦，便于替换数据源和模型。
2. 用 `skills` 封装高频分析动作，减少 Agent 直接拼装底层工具的复杂度。
3. 支持从数据清洗、模型训练到投研报告生成的端到端流程。

## 2. 当前项目结构

```text
Finance/
├── apps/
│   └── Financial-MCP-Agent/         # 多智能体投研主应用
├── services/
│   └── a-share-mcp-is-just-i-need/  # A股 MCP 服务（原子工具层）
├── pipelines/
│   ├── preprocessing/               # 数据清洗、去重
│   ├── training/                    # 训练脚本
│   └── evaluation/                  # 评估脚本
├── data/
│   ├── nasdaq_news_sentiment/       # 情感数据与样例
│   └── risk_nasdaq/                 # 风险数据与样例
├── tools/
│   └── download_qwen.py             # 模型下载工具
├── docs/
│   ├── notes/                       # 历史改造说明
│   └── skills/                      # skills 体系文档
└── requirements.txt
```

## 3. 系统分层设计

### 3.1 数据与工具层（MCP）

`services/a-share-mcp-is-just-i-need` 暴露原子工具：
- 行情与K线：`get_historical_k_data`, `get_adjust_factor_data`
- 财报与指标：`get_profit_data`, `get_cash_flow_data`, `get_dupont_data` 等
- 市场与指数：`get_hs300_stocks`, `get_sz50_stocks`, `get_zz500_stocks`
- 新闻：`crawl_news`

这些工具只关注“准确拿数”。

### 3.2 业务技能层（Skills）

`apps/Financial-MCP-Agent/src/skills` 将多个原子工具封装成高层技能：
- `company_profile_skill`
- `fundamental_analysis_skill`
- `technical_analysis_skill`
- `valuation_analysis_skill`
- `news_analysis_skill`

新增 `contracts.py` 用于定义每个 skill 的工具契约（必需工具 + 可选工具）；`registry.py` 会在运行时校验工具可用性，不满足契约时自动跳过并记录原因。

### 3.3 智能体层（Agents）

主应用中包含 `fundamental / technical / value / news / summary` 五类 Agent：
- 前四类 Agent 负责并行分析
- `summary_agent` 汇总并输出最终报告

每个 Agent 的工具包由 `skills + raw fallback tools` 组成：
- 优先调用 skill 完成首轮结构化采集
- 再按需回退到原子工具补细节

### 3.4 编排层（LangGraph）

主流程（`apps/Financial-MCP-Agent/src/main.py`）通过图编排执行：
1. 解析输入（股票代码/公司名）
2. 并行执行四类分析 Agent
3. 汇总 Agent 生成报告
4. 落盘报告与执行日志

## 4. 关键运行路径

### 4.1 启动主应用

在项目根目录：

```bash
python apps/Financial-MCP-Agent/src/main.py --command "分析茅台基本面和估值"
```

### 4.2 环境变量

主应用支持通过环境变量指定 MCP 服务位置：

```bash
A_SHARE_MCP_SERVER_DIR=E:/Learning/Finance/services/a-share-mcp-is-just-i-need
A_SHARE_MCP_COMMAND=uv
A_SHARE_MCP_ENTRY=mcp_server.py
```

### 4.3 训练与评估

```bash
python pipelines/training/train_qwen_sentiment.py
python pipelines/training/train_qwen_risk.py
python pipelines/evaluation/test_qwen_sentiment.py
python pipelines/evaluation/test_risk_model.py
```

## 5. skills 扩展方法

新增 skill 推荐流程：
1. 在 `src/skills/` 新建 skill 文件并定义 `@tool("your_skill_name")`
2. 在 `contracts.py` 注册 skill 契约
3. 在 `registry.py` 的 `SKILL_NAME_MAP` 与 `AGENT_SKILLS` 中挂载
4. 在对应 agent prompt 中加入“优先使用该 skill”的调用指令

## 6. 重构说明

本次重构聚焦两件事：
1. 目录清晰化：将应用、服务、数据、流水线、工具、文档明确分层。
2. skills 工程化：新增 skill 契约与可用性校验，降低运行时工具缺失导致的故障概率。

详细 skill 文档见：`docs/skills/SKILL_SYSTEM.md`。
