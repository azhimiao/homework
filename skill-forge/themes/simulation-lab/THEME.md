---
title: 工科仿真实验
tags: [simulation, matlab, multisim, keil, stem]
status: stable
version: "2.0"
---

# Theme: simulation-lab v2

**已合并至 homework-assistant**。本 theme 提供仿真实验 **lab skill**；路由请用 `homework-assistant` 或别名 `simulation-homework-assistant`。

## Skills

| 源文件 | 作用 |
|--------|------|
| `simulation-homework-assistant.skill.md` | homework-assistant 别名 |
| `matlab-simulink-lab.skill.md` | MATLAB/Simulink |
| `multisim-lab.skill.md` | Multisim |
| `keil-embedded-lab.skill.md` | Keil 嵌入式 |

## 编译

```bash
python skill-core/skill.py batch build simulation-lab --test
```

安装入口推荐：`examples/homework-assistant`（覆盖仿真 + 计组 + 编程）。
