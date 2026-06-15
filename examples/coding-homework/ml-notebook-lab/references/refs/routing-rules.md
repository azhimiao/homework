# 编程作业路由规则

同 student-homework：读 `assignment-catalog.yaml`，打分 → **用户确认** → install → handoff。

## 匹配

- score = keyword_hits × 2 + major_match × 3
- min_score ≥ 2；tie ≤ 1 → ASK

## 与 student-homework 关系

- **FPGA/Quartus** → 仍用 `student-homework` / `homework-assistant`
- **编程/算法/ML** → 本 theme `coding-homework-assistant`

`homework-assistant` 的 resolve_order 已含 `skill-forge/built/coding-homework/{skill}`，catalog 合并后亦可统一入口。

## handoff

| skill | 首问 |
|-------|------|
| python-lab | assignment 描述 + Python 版本 |
| java-oop-lab | lab 要求 + JDK/Maven |
| ds-algorithm-lab | 算法题 + 语言 python/java |
| ml-notebook-lab | 数据集 + 模型任务 |

## 学术诚信

- 禁止代考、抄袭、伪造运行结果
- 协助理解、调试、结构、报告 — 作者须理解并能复述代码
