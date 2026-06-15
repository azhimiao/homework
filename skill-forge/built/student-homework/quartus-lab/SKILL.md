---
name: quartus-lab
description: >-
  Accurate Intel Quartus Prime lab workflow: detect toolchain, select correct MAX10/Cyclone
  device per board, assign pins from board manual, compile, program, simulate, draft report.
  Use when after homework-assistant routes 计组/FPGA work, or direct Quartus request.
  Triggers: "Quartus", "计组实验", "FPGA", "Verilog", "DE10-Lite", "引脚", "Programmer".
metadata:
  version: "2.0.0"
  status: stable
  protocol: skill-protocol-v2
compatibility: run check_quartus.py first; no fabricated compile success
---

# Quartus Lab

## Quick Start

1. READ refs/quartus-setup.md and refs/board-devices.yaml
2. RUN python scripts/check_quartus.py; PARSE QUARTUS_PATH; IF QUARTUS_NOT_FOUND → guide install; STOP
3. ASK board if unset; LOOKUP family+device from board-devices.yaml; REJECT wrong family (e.g. Cyclone on DE10-Lite)
4. ASK lab_task and read handout if provided
5. CREATE project_path; GUIDE New Project Wizard with exact Family and Device strings

## Workflow

### Step 1
READ refs/quartus-setup.md and refs/board-devices.yaml

### Step 2
RUN python scripts/check_quartus.py; PARSE QUARTUS_PATH; IF QUARTUS_NOT_FOUND → guide install; STOP

### Step 3
ASK board if unset; LOOKUP family+device from board-devices.yaml; REJECT wrong family (e.g. Cyclone on DE10-Lite)

### Step 4
ASK lab_task and read handout if provided

### Step 5
CREATE project_path; GUIDE New Project Wizard with exact Family and Device strings

### Step 6
WRITE or edit HDL under src/; top module name = project name

### Step 7
READ refs/board-pins/{board}.md if exists; WRITE docs/pin-assignment.md; APPLY Pin Planner or QSF assignments

### Step 8
RUN `quartus_sh --flow compile {project}`; CAPTURE output to docs/build-log.txt

### Step 9
IF errors → fix HDL or pins; retry up to 3 times; do not claim success without 0 errors

### Step 10
IF simulation required → guide University Program VWF; LIST docs/screenshots-needed.md

### Step 11
IF program to board → Tools → Programmer, select USB-Blaster, .sof from output_files/

### Step 12
DRAFT docs/lab-report-draft.md; SYNC homework/checklist.md deliverables

### Decision logic

```
IF board unknown → ASK; never pick random device
IF DE10-Lite → device MUST be 10M50DAF484C7G MAX 10
IF compile fails → parse build-log; no fake waveforms
IF timing fails only → note in report; functional compile sufficient for most labs
IF pin Mismatch → reconcile with Terasic manual before recompile
IF lab_task vague → ask for 实验指导书 section
```

## Outputs

Profile: `hybrid`

Return artifacts plus a narrative summary.

## Tools

| ID | Use | Constraints |
|----|-----|-------------|
| shell |  |  |
| file_read |  |  |
| file_write |  |  |
| ask_user |  |  |
| web_fetch |  |  |

## Failure Modes

| ID | Signal | Recovery |
|----|--------|----------|
| F1 | QUARTUS_NOT_FOUND | install Lite + device support |
| F2 | wrong FPGA family for board | fix per board-devices.yaml |
| F3 | illegal or conflicting pins | fix pin-assignment.md |
| F4 | HDL/elaboration fail | fix from build-log |
| F5 | cannot infer design | ask handout |

## Dependencies

- `skill-core`
- `homework-assistant`

## Additional Resources

- [IR source](references/ir.md)
