# Keil MDK / 嵌入式

## 检测

```bash
python scripts/check_keil.py
```

## MCU 参考（须与 handout 一致）

| kit_id | MCU | 说明 |
|--------|-----|------|
| STM32F103C8 | STM32F103C8T6 | Blue Pill / 最小系统板 |
| STM32F407 | STM32F407VGT6 | Discovery / 常见课设 |
| AT89C51 | 8051 | 51 单片机基础 |
| STM32F103RC | STM32F103RCT6 | 正点原子等 |

**禁止**随意换型号而不改启动文件/链接脚本。

## 工程结构

```
homework/keil-lab/{project}/
├── MDK-ARM/*.uvprojx
├── Core/Src, Inc
├── docs/pin-map.md
├── outputs/build.log
└── docs/report.md
```

## 流程

1. 选择 Device（Pack 已安装）
2. 配置 clock、GPIO（对照原理图）
3. Build (F7) → 0 Error(s)
4. Download / 仿真

## Pack

STM32 需 `Keil.STM32F1xx_DFP` 等；未装 Pack → 引导 Pack Installer

## 引脚

写入 `docs/pin-map.md`；对照开发板 silk/手册
