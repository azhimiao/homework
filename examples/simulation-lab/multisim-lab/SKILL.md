---
name: multisim-lab
description: >-
  Complete NI Multisim circuit simulation lab: verify install, build circuit, run
  interactive sim, waveform capture, component table, report. Use when 电路分析, 模拟电路, Multisim.
  After homework-assistant routes (unified catalog).
metadata:
  version: "1.0.0"
  status: stable
  protocol: skill-protocol-v2
compatibility: check_multisim.py
---

# Multisim Lab

## Quick Start

1. READ refs/multisim-setup.md, report-template.md
2. RUN scripts/check_multisim.py; IF MULTISIM_NOT_FOUND → guide NI install; STOP
3. ASK lab_task; READ handout schematic requirements
4. GUIDE place components; WRITE docs/components.md (RefDes, value)
5. RUN interactive simulation; CAPTURE oscilloscope to outputs/waveforms/

## Workflow

### Step 1
READ refs/multisim-setup.md, report-template.md

### Step 2
RUN scripts/check_multisim.py; IF MULTISIM_NOT_FOUND → guide NI install; STOP

### Step 3
ASK lab_task; READ handout schematic requirements

### Step 4
GUIDE place components; WRITE docs/components.md (RefDes, value)

### Step 5
RUN interactive simulation; CAPTURE oscilloscope to outputs/waveforms/

### Step 6
VERIFY DC paths and grounds before claiming success

### Step 7
DRAFT docs/report.md per report-template; UPDATE checklist

### Decision logic

```
IF missing ground → fix before delivery
IF component values differ from handout → document in report
IF fabricated waveform → refuse F4
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
| F1 | MULTISIM_NOT_FOUND | install Multisim |
| F2 | circuit error | fix wiring/values |
| F3 | no spec | ask handout |
| F4 | fake scope | rerun simulation |

## Dependencies

- `skill-core`
- `homework-assistant`

## Additional Resources

- [IR source](references/ir.md)
