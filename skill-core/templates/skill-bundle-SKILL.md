---
name: skillforskill-md-bundle
description: >-
  Markdown-only bundle of SkillForSkill Agent Skills. Use when user browses the skill/
  folder, wants to pick a skill by topic, or read SKILL.md without yaml/py toolchain.
  Triggers: skill catalog, 选 skill, 有哪些 skill, relationship-match, 作业路由.
metadata:
  version: "1.0.0"
  status: stable
  protocol: skill-protocol-v2
compatibility: read-only; install full skills from github-upload with skill-core
---

# SkillForSkill Markdown Bundle

## Quick Start

1. 本目录为 **纯 Markdown 导出包**（与 `github-upload` 内容对应）。
2. 每个可安装 skill 位于 **`examples/<theme>/<skill-name>/SKILL.md`**（与 skill-forge theme 同构）。
3. 主题源文件位于 **`skill-forge/themes/<theme>/`**。
4. 完整安装需 `github-upload` + `skill-core`：

```bash
python skill-core/skill.py install examples/student-homework/homework-assistant --host cursor --scope global
python skill-core/skill.py install examples/research/research-survey --host cursor --scope global
```

## 按主题选 Skill

| 需求 | 路径 |
|------|------|
| 理工科作业 | `examples/student-homework/homework-assistant/SKILL.md` |
| 科研套件 | `examples/research/research-survey/SKILL.md` |
| 婚恋 / 理想伴侣（单人） | `examples/relationship/relationship-match/SKILL.md` |
| AI 恋人长期记忆 | `examples/companion-memory/companion-memory/SKILL.md` |
| 双人关系兼容 | `examples/couple-compatibility/couple-intake/SKILL.md` |
| 职业规划 | `examples/career-match/career-match/SKILL.md` |
| 编程作业 | `examples/homework-assistant/SKILL.md`（统一入口，含编程路由） |
| 仿真实验 | `examples/homework-assistant/SKILL.md`（同上；别名 `simulation-homework-assistant`） |
| 综合作业 / 理工科 | `examples/homework-assistant/SKILL.md` |
| 课程报告 | `examples/course-report/SKILL.md` |
| 政策简报 | `examples/policy-brief/SKILL.md` |
| 求职准备 | `examples/job-prep-assistant/SKILL.md` |
| 理财风格 | `examples/finance-style-survey/SKILL.md` |
| 健康习惯 | `examples/health-habit-coach/SKILL.md` |
| 团队协作 | `examples/team-collab-profile/SKILL.md` |
| 科研调查 | `examples/research-survey/SKILL.md` |

完整列表见 **`INDEX.md`**、**`ROADMAP.md`**。

## Workflow

READ `INDEX.md` → open `examples/<skill-name>/SKILL.md` → optional `references/`

## Failure Modes

| ID | Signal | Recovery |
|----|--------|----------|
| F1 | skill-not-found | list INDEX.md |
| F2 | needs-yaml-or-script | use github-upload full repo |
