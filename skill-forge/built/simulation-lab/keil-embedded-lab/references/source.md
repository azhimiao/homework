---
name: keil-embedded-lab
profile: hybrid
status: stable
version: "1.0.0"
invocation: auto
host: any
---

# Goal
Complete Keil MDK embedded lab: verify Keil, select exact MCU from mcu-devices.yaml, configure project, build 0 errors, pin map, report.

# Context
单片机, STM32, 8051, Keil uVision. After homework-assistant routes (unified catalog).

# Constraints
- 精度：mcu-devices.yaml + keil-setup.md; Device must match board
- 工具：check_keil.py; no fabricated build log

# Inputs
## Required
- lab_task: string

## Optional
- mcu: string — default from catalog or ASK
- project_path, handout, keil_path

# Outputs
**Profile:** hybrid

1. Keil `.uvprojx` under homework/keil-lab/
2. `Core/Src`, `Core/Inc`
3. `docs/pin-map.md`, `outputs/build.log`
4. `docs/report.md`

# Steps
1. READ refs/keil-setup.md, mcu-devices.yaml, report-template.md
2. RUN scripts/check_keil.py; IF KEIL_NOT_FOUND → guide MDK install; STOP
3. ASK mcu kit and lab_task; READ handout
4. LOOKUP mcu_part in mcu-devices.yaml; CREATE uVision .uvprojx project with exact Device
5. IMPLEMENT GPIO/timer/UART per lab; WRITE docs/pin-map.md
6. BUILD project; CAPTURE build log to outputs/build.log; require 0 Error(s)
7. IF download required → guide ST-Link/J-Link; document observed behavior
8. DRAFT report; UPDATE checklist

# Decision
IF mcu unknown → ASK; never guess STM32 variant
IF Pack missing → guide Pack Installer
IF build errors → fix before delivery
IF wrong device in project → change per mcu-devices.yaml

# Tools
- shell — check_keil.py
- file_read, file_write, ask_user

# Failures
F1: keil-missing | KEIL_NOT_FOUND | install MDK
F2: device-mismatch | wrong MCU selected | fix per mcu-devices.yaml
F3: build-fail | compile errors | fix from build.log
F4: vague-task | no spec | ask handout
F5: fabricated-build | fake 0 errors | rebuild and log

# Deps
depends_on:
  - skill-core
  - homework-assistant
provides:
  - keil-embedded-lab

# Version
version: "1.0.0"
status: stable
