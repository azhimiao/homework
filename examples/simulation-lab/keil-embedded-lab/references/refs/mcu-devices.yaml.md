# MD 兼容视图 — `mcu-devices.yaml`

> **权威源文件**：同目录 `mcu-devices.yaml`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `yaml` |
| 路径 | `refs/mcu-devices.yaml` |
| 用途 | MCU 器件对照表。 |

## 内容

```yaml
# MCU / 开发板器件表

与 keil-setup.md 配合；**以实验指导书为准**。

| board | mcu_part | pack_hint |
|-------|----------|-----------|
| STM32F103C8 最小系统 | STM32F103C8T6 | STM32F1xx_DFP |
| STM32F407 探索板 | STM32F407VGT6 | STM32F4xx_DFP |
| STC89C52 51 最小系统 | AT89C52 | 8051 无 DFP 时选 Generic 8051 |
| Arduino UNO (avr, 非 Keil 主路径) | ATmega328P | 若 handout 指定 Arduino 则换 toolchain |

Keil skill 默认 STM32；51 实验须 explicit 选择。
```
