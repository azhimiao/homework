# 仿真实验路由（已合并至 homework-assistant）

**入口已统一**：`homework-assistant`（student-homework）的 `assignment-catalog.yaml` v3。

本 theme 的 `simulation-homework-assistant` 为**别名 skill**，行为与 homework-assistant 相同。

## 子 lab skill（ready）

| skill | 检测脚本 |
|-------|----------|
| matlab-simulink-lab | check_matlab.py |
| multisim-lab | 用户确认 Multisim |
| keil-embedded-lab | 用户确认 Keil |

install 路径：`skill-forge/built/simulation-lab/{skill}`

## planned 工具

LTspice、Proteus、LabVIEW 等 → homework-assistant 走 `universal-stem-workflow.md`，不 install。

## handoff

| skill | 首问 |
|-------|------|
| matlab-simulink-lab | 实验内容 + MATLAB 版本 |
| multisim-lab | 电路任务 + Multisim 版本 |
| keil-embedded-lab | MCU 型号 + 实验要求 |

报告：六段式见 `report-template.md`
