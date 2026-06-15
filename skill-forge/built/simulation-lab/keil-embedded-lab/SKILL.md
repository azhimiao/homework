---
name: keil-embedded-lab
description: >-
  Complete Keil MDK embedded lab: verify Keil, select exact MCU from mcu-devices.yaml,
  configure project, build 0 errors, pin map, report. Use when 单片机, STM32, 8051, Keil
  uVision. After homework-assistant routes (unified catalog).
metadata:
  version: "1.0.0"
  status: stable
  protocol: skill-protocol-v2
compatibility: check_keil.py; no fabricated build log
---

# Keil Embedded Lab

## Quick Start

1. READ refs/keil-setup.md, mcu-devices.yaml, report-template.md
2. RUN scripts/check_keil.py; IF KEIL_NOT_FOUND → guide MDK install; STOP
3. ASK mcu kit and lab_task; READ handout
4. LOOKUP mcu_part in mcu-devices.yaml; CREATE uVision .uvprojx project with exact Device
5. IMPLEMENT GPIO/timer/UART per lab; WRITE docs/pin-map.md

## Workflow

### Step 1
READ refs/keil-setup.md, mcu-devices.yaml, report-template.md

### Step 2
RUN scripts/check_keil.py; IF KEIL_NOT_FOUND → guide MDK install; STOP

### Step 3
ASK mcu kit and lab_task; READ handout

### Step 4
LOOKUP mcu_part in mcu-devices.yaml; CREATE uVision .uvprojx project with exact Device

### Step 5
IMPLEMENT GPIO/timer/UART per lab; WRITE docs/pin-map.md

### Step 6
BUILD project; CAPTURE build log to outputs/build.log; require 0 Error(s)

### Step 7
IF download required → guide ST-Link/J-Link; document observed behavior

### Step 8
DRAFT report; UPDATE checklist

### Decision logic

```
IF mcu unknown → ASK; never guess STM32 variant
IF Pack missing → guide Pack Installer
IF build errors → fix before delivery
IF wrong device in project → change per mcu-devices.yaml
```

## Outputs

Profile: `hybrid`

Return artifacts plus a narrative summary.

## Tools

| ID | Use | Constraints |
|----|-----|-------------|
| shell |  |  |
| file_read, |  |  |

## Failure Modes

| ID | Signal | Recovery |
|----|--------|----------|
| F1 | KEIL_NOT_FOUND | install MDK |
| F2 | wrong MCU selected | fix per mcu-devices.yaml |
| F3 | compile errors | fix from build.log |
| F4 | no spec | ask handout |
| F5 | fake 0 errors | rebuild and log |

## Dependencies

- `skill-core`
- `homework-assistant`

## Additional Resources

- [IR source](references/ir.md)
