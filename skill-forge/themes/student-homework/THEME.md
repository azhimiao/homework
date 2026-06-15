---
title: 学生作业 / 理工科统一入口
tags: [student, homework, quartus, fpga, matlab, stem, routing]
status: stable
version: "3.0"
---

# Theme: 理工科作业 v3

**专业 + 作业** → 统一 catalog（FPGA + 编程 + 仿真 + planned 工科工具）→ **确认** → install lab skill 或通用工作流。

## Skills

| 源文件 | 作用 |
|--------|------|
| `homework-assistant.skill.md` | **唯一主入口**：路由、确认、install、handoff |
| `quartus-lab.skill.md` | 计组 / Quartus |

仿真 lab skill 在 `simulation-lab` theme 构建，由 catalog `resolve_order` 安装。

## 关键 refs

| 文件 | 内容 |
|------|------|
| `refs/assignment-catalog.yaml` | v3 统一路由表 |
| `refs/stem-tool-matrix.md` | ready / planned 工具矩阵 |
| `refs/universal-stem-workflow.md` | 无 lab skill 时的流程 |
| `refs/routing-rules.md` | 打分与确认 |

## 编译

```bash
python skill-core/skill.py batch build student-homework --test
python skill-core/skill.py batch build simulation-lab --test
python skill-core/skill.py batch build coding-homework --test
python skill-core/skill.py install examples/student-homework/homework-assistant --host cursor --scope global
```

## 示例

> 自动化，自动控制 Simulink 阶跃响应实验  

→ `matlab-control-lab` → 确认 → `matlab-simulink-lab`

> 机械工程，ANSYS 静力分析  

→ `ansys-fea-lab` (planned) → checklist + universal-stem-workflow
