keil-embedded-lab

---

# 0. Compilation Target

```yaml
host: any
invocation: auto
output_profile: hybrid
```

---

# 1. Intent（意图）

Theme: simulation-lab

## Goal
Complete Keil MDK embedded lab: verify Keil, select exact MCU from mcu-devices.yaml, configure project, build 0 errors, pin map, report.

## Context
单片机, STM32, 8051, Keil uVision. After homework-assistant routes (unified catalog).

## Constraints
- 精度：mcu-devices.yaml + keil-setup.md; Device must match board
- 工具：check_keil.py; no fabricated build log

---

# 2. Inputs（输入定义）

## Required Inputs
## Required
- lab_task: string

## Optional
- mcu: string — default from catalog or ASK
- project_path, handout, keil_path

---

# 3. Outputs（输出定义）

**Profile:** hybrid

1. Keil `.uvprojx` under homework/keil-lab/
2. `Core/Src`, `Core/Inc`
3. `docs/pin-map.md`, `outputs/build.log`
4. `docs/report.md`

---

# 5. Execution Plan（执行流程）

1. READ refs/keil-setup.md, mcu-devices.yaml, report-template.md
2. RUN scripts/check_keil.py; IF KEIL_NOT_FOUND → guide MDK install; STOP
3. ASK mcu kit and lab_task; READ handout
4. LOOKUP mcu_part in mcu-devices.yaml; CREATE uVision .uvprojx project with exact Device
5. IMPLEMENT GPIO/timer/UART per lab; WRITE docs/pin-map.md
6. BUILD project; CAPTURE build log to outputs/build.log; require 0 Error(s)
7. IF download required → guide ST-Link/J-Link; document observed behavior
8. DRAFT report; UPDATE checklist

---

# 6. Decision Logic（决策系统）

```
IF mcu unknown → ASK; never guess STM32 variant
IF Pack missing → guide Pack Installer
IF build errors → fix before delivery
IF wrong device in project → change per mcu-devices.yaml
```

---

# 7. Tool / API Binding（工具绑定）

| Portable ID | Use | Constraints |
|-------------|-----|-------------|
| shell | | |
| file_read, | | |

---

# 10. Failure Modes（失败模式）

## F1: keil-missing
- Signal: KEIL_NOT_FOUND
- Recovery: install MDK
- Severity: block

## F2: device-mismatch
- Signal: wrong MCU selected
- Recovery: fix per mcu-devices.yaml
- Severity: block

## F3: build-fail
- Signal: compile errors
- Recovery: fix from build.log
- Severity: block

## F4: vague-task
- Signal: no spec
- Recovery: ask handout
- Severity: block

## F5: fabricated-build
- Signal: fake 0 errors
- Recovery: rebuild and log
- Severity: block

---

# 12. Skill Graph Dependencies（依赖）

```yaml
depends_on:
  - skill-core
  - homework-assistant
provides:
  - keil-embedded-lab
```

---

# 13. Versioning（版本系统）

```yaml
version: "1.0.0"
status: stable
```
