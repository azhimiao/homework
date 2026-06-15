---
name: simulation-homework-assistant
description: >-
  Alias of homework-assistant for simulation triggers (MATLAB, Simulink, Multisim, Keil).
  **Delegate entirely** to homework-assistant v3 unified catalog — same confirm → install →
  handoff; no separate simulation-lab catalog. Use when triggers: MATLAB实验, Simulink,
  Multisim, 电路仿真, Keil, 单片机实验, 自动控制实验. User may install this skill or homework-assistant;
  behavior identical.
metadata:
  version: "2.0.0"
  status: stable
  protocol: skill-protocol-v2
---

# Simulation Homework Assistant

## Quick Start

1. DELEGATE to homework-assistant workflow (Steps 1–11); WRITE homework/session.yaml
2. READ student-homework refs/assignment-catalog.yaml, routing-rules.md, stem-tool-matrix.md
3. MATCH matlab-control-lab, multisim-circuit-lab, keil-embedded-lab or planned spice/proteus/labview entries
4. CONFIRM → install matlab-simulink-lab, multisim-lab, keil-embedded-lab via resolve_order (simulation-lab built path)
5. WRITE homework/checklist.md; HANDOFF to installed lab skill with lab_task

## Workflow

### Step 1
DELEGATE to homework-assistant workflow (Steps 1–11); WRITE homework/session.yaml

### Step 2
READ student-homework refs/assignment-catalog.yaml, routing-rules.md, stem-tool-matrix.md

### Step 3
MATCH matlab-control-lab, multisim-circuit-lab, keil-embedded-lab or planned spice/proteus/labview entries

### Step 4
CONFIRM → install matlab-simulink-lab, multisim-lab, keil-embedded-lab via resolve_order (simulation-lab built path)

### Step 5
WRITE homework/checklist.md; HANDOFF to installed lab skill with lab_task

### Decision logic

```
IF user declines confirm → block install
IF FPGA/quartus → same catalog routes comp-org-quartus → quartus-lab
IF pure coding → same catalog routes python/java/ds/ml labs
IF install fails → manual command with skill-forge/built/simulation-lab path
IF planned-tool match → universal-stem-workflow; no install
```

## Outputs

Profile: `hybrid`

Return artifacts plus a narrative summary.

## Tools

| ID | Use | Constraints |
|----|-----|-------------|
| ask_user, |  |  |

## Failure Modes

| ID | Signal | Recovery |
|----|--------|----------|
| F1 | score below min_score | stem-tool-matrix + clarify |
| F2 | CLI error | manual command |
| F3 | tie | user choose |
| F4 | user did not confirm | block install |
| F5 | ltspice proteus labview planned | universal-stem-workflow; no install |

## Dependencies

- `skill-core`
- `homework-assistant`

## Additional Resources

- [IR source](references/ir.md)
