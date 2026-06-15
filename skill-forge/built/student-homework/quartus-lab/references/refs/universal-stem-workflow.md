# 无专用 lab skill 时的理工科实验工作流

当 catalog 条目 `status: planned` 或未匹配到 ready skill 时使用。

## Step 1 — 锁定工具与环境

- ASK：软件全名、版本、操作系统、是否有实验指导书
- READ `stem-tool-matrix.md` 对应行
- RUN 环境检测（若 theme 有 `scripts/check_*.py`）；否则 ASK 用户在本机确认「能否打开软件」

## Step 2 — 拆解 deliverables

从作业/指导书提取：

- 输入（数据、器件、参数）
- 输出（工程文件、图表、报告章节）
- 评分 rubric（若有）

WRITE `homework/checklist.md`，每项可勾选。

## Step 3 — 文件优先协助

Agent **优先**编辑用户可版本管理的文件：

| 类型 | 示例 |
|------|------|
| 源码/脚本 | `.v`, `.py`, `.m`, `.c`, `.tcl` |
| 工程/配置 | `.qsf`, `.uvprojx`, `.slx`, `.json`, `.yaml` |
| 网表/SPICE | `.cir`, `.asc` |
| 文档 | `docs/params.md`, `docs/report.md` |

GUI 操作（拖拽元件、点菜单）→ 写**逐步点击清单**，由用户在本机执行；Agent 不声称已完成未验证的步骤。

## Step 4 — 运行与证据

- 能 CLI/Batch 的 → 给出命令，CAPTURE log
- 仅 GUI 的 → `docs/screenshots-needed.md` 列出必拍截图
- **禁止**伪造波形、编译成功、仿真结果

## Step 5 — 报告

统一六段式（见各 theme `report-template.md` 若存在）：

1. 目的 2. 原理 3. 步骤 4. 结果 5. 分析 6. 结论

## Step 6 — 升级路径

若某工具使用频繁，在仓库提 issue：「为 {tool} 添加 lab skill」，参照 `quartus-lab` / `matlab-simulink-lab` 模式。
