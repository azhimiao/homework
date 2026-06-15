---
name: matlab-simulink-lab
description: >-
  Complete MATLAB/Simulink control or signal labs: verify MATLAB, build .m/.slx, run
  simulation, capture plots, params doc, report per report-template.md. Use when after
  homework-assistant routes (unified STEM catalog). Triggers: 自动控制原理, Simulink, 阶跃响应, PID.
metadata:
  version: "1.0.0"
  status: stable
  protocol: skill-protocol-v2
compatibility: check_matlab.py first
---

# Matlab Simulink Lab

## Quick Start

1. READ refs/matlab-simulink-setup.md, report-template.md
2. RUN scripts/check_matlab.py; IF MATLAB_NOT_FOUND → guide install; STOP
3. ASK lab_task; READ handout
4. CREATE project under homework/matlab-lab/
5. IMPLEMENT .m or .slx; RECORD params in docs/params.md

## Workflow

### Step 1
READ refs/matlab-simulink-setup.md, report-template.md

### Step 2
RUN scripts/check_matlab.py; IF MATLAB_NOT_FOUND → guide install; STOP

### Step 3
ASK lab_task; READ handout

### Step 4
CREATE project under homework/matlab-lab/

### Step 5
IMPLEMENT .m or .slx; RECORD params in docs/params.md

### Step 6
RUN simulation; SAVE figures to outputs/figures/

### Step 7
IF Simulink → verify solver settings match handout

### Step 8
DRAFT docs/report.md; UPDATE checklist

### Decision logic

```
IF lab_task vague → ASK handout
IF simulation diverges from theory → note in analysis section
IF user claims results without run → refuse fabricated plots
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
| F1 | MATLAB_NOT_FOUND | install MATLAB |
| F2 | model does not run | fix equations/blocks |
| F3 | no spec | ask handout |
| F4 | no run claimed | rerun and capture |

## Dependencies

- `skill-core`
- `homework-assistant`

## Additional Resources

- [IR source](references/ir.md)
