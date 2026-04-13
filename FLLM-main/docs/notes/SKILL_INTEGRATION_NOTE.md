# Finance 项目打包说明

本打包基于原始 `Finance` 项目，已将其中的 `Financial-MCP-Agent` 替换为新增 Skills 分层后的版本。

当前状态（重构后目录）：
- `apps/Financial-MCP-Agent/`：已完成 Skills 增强改造（保留 MCP，新增 `src/skills/`，并让四个分析 Agent 优先走 skill）。
- `services/a-share-mcp-is-just-i-need/`：保持原始版本，尚未按同步改造方案落地代码。

如需继续同步升级服务端，可参考后续的 `a-share-mcp-is-just-i-need` 分层改造方案另行实现。
