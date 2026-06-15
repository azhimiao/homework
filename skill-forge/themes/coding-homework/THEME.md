---
title: 编程课作业
tags: [coding, python, java, homework, router]
status: stable
version: "1.0"
---

# Theme: coding-homework（路线图 #3）

专业 + 编程作业描述 → 确认 → 安装 **python-lab / java-oop-lab / ds-algorithm-lab / ml-notebook-lab**。

## Skills

| 源文件 | 作用 |
|--------|------|
| `coding-homework-assistant.skill.md` | 路由 + install |
| `python-lab.skill.md` | Python 程设 |
| `java-oop-lab.skill.md` | Java OOP |
| `ds-algorithm-lab.skill.md` | 数据结构/算法 |
| `ml-notebook-lab.skill.md` | ML / Notebook 课设 |

## 与 student-homework

- **Quartus/FPGA** → `homework-assistant`（student-homework）
- **编程类** → 本 theme `coding-homework-assistant`

## 编译

```bash
python skill-core/skill.py batch build coding-homework --test
python skill-core/skill.py install examples/coding-homework-assistant --host cursor --scope global
```

## 规范

- `refs/python-standards.md` — PEP 8
- `refs/java-standards.md` — JUnit/Maven
- `scripts/check_python.py`, `check_java.py`
