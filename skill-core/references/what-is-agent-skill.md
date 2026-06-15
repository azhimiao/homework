# What Is an Agent Skill?

**Agent Skill** 不是某个 IDE 的私有功能，而是 2025 年底开源的 **Agent Skills 开放标准**（[agentskills.io](https://agentskills.io)）。

## 一句话

一个 Skill = **一个文件夹 + 一份 `SKILL.md`**，用来教 AI Agent 如何完成某类特定任务。

## 和 Prompt / Rule 的区别

| | Prompt | Rule | Agent Skill |
|---|--------|------|-------------|
| 形态 | 一次性对话 | 项目配置文件 | 可版本化的能力包 |
|  portability | 低 | 绑定工具 | 跨工具复用 |
| 结构 | 自由文本 | 自由文本 | 标准 frontmatter + 正文 + 可选 scripts/references |
| 加载方式 | 手动粘贴 | 自动注入 | 渐进披露（元数据 → 正文 → 引用文件） |

## 谁在用

同一套 `SKILL.md` 可被多个 Agent 产品加载，例如：

- Cursor（`.cursor/skills/` 或 `~/.cursor/skills/`）
- Claude Code（`~/.claude/skills/`）
- 其他兼容 Agent Skills 规范的工具（`.agents/skills/` 等）

**Skill-Core 面向的是写 Skill 的开发者**，不是某一个 Agent 产品。

## 文件结构（开放标准）

```
my-skill/
├── SKILL.md          # 必需：元数据 + 执行指令
├── references/       # 可选：详细文档，按需加载
├── scripts/          # 可选：可执行脚本
└── assets/           # 可选：模板、静态资源
```

## SKILL.md 最小格式

```markdown
---
name: my-skill
description: What it does and when to use it. Third person. Include trigger terms.
---

# My Skill

## Quick Start
1. Step one
2. Step two
```

## Skill-Core 在这套生态里的位置

```
开发者 Intent
    ↓
Skill-Core IR（13 节设计稿）
    ↓
SKILL.md（开放标准运行时）
    ↓
任意兼容 Agent 加载执行
    ↓
评估 + 迭代
```

Skill-Core 是 **Skill 编译器 + 参考实现**，产出物遵循：

- 运行时：[Agent Skills 开放标准](https://agentskills.io)
-  authoring：[Skill Protocol Standard](../docs/optional/STANDARD.md)（可选参考）
