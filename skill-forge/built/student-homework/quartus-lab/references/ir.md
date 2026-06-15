quartus-lab

---

# 0. Compilation Target

```yaml
host: any
invocation: auto
output_profile: hybrid
```

---

# 1. Intent（意图）

Theme: student-homework

## Goal
Accurate Intel Quartus Prime lab workflow: detect toolchain, select correct MAX10/Cyclone device per board, assign pins from board manual, compile, program, simulate, draft report.

## Context
After homework-assistant routes 计组/FPGA work, or direct Quartus request. Triggers: "Quartus", "计组实验", "FPGA", "Verilog", "DE10-Lite", "引脚", "Programmer".

## Constraints
- 时间：one lab focus per session
- 精度：device from board-devices.yaml; pins from board-pins/*.md or Terasic manual — never guess
- 工具限制：run check_quartus.py first; no fabricated compile success

---

# 2. Inputs（输入定义）

## Required Inputs
## Required
- lab_task: string — 实验要求（如 ALU、交通灯、计数器）

## Optional
- board: string — DE10-Lite | DE1-SoC | DE2-115 | DE10-Standard | DE0-CV — default from catalog default_board or ASK
- language: enum — verilog | vhdl | bdf — default: verilog
- project_path: path — default: homework/comp-org-lab/{project_name}/
- quartus_path: path — from check_quartus.py if not on PATH

---

# 3. Outputs（输出定义）

**Profile:** hybrid

1. Quartus project (.qpf, .qsf, src/*.v)
2. `docs/pin-assignment.md` — signal → PIN table
3. `docs/build-log.txt` — compile output
4. `docs/lab-report-draft.md` — 六段报告草稿
5. `docs/screenshots-needed.md` — RTL / waveform / Programmer 清单

---

# 5. Execution Plan（执行流程）

1. READ refs/quartus-setup.md and refs/board-devices.yaml
2. RUN python scripts/check_quartus.py; PARSE QUARTUS_PATH; IF QUARTUS_NOT_FOUND → guide install; STOP
3. ASK board if unset; LOOKUP family+device from board-devices.yaml; REJECT wrong family (e.g. Cyclone on DE10-Lite)
4. ASK lab_task and read handout if provided
5. CREATE project_path; GUIDE New Project Wizard with exact Family and Device strings
6. WRITE or edit HDL under src/; top module name = project name
7. READ refs/board-pins/{board}.md if exists; WRITE docs/pin-assignment.md; APPLY Pin Planner or QSF assignments
8. RUN `quartus_sh --flow compile {project}`; CAPTURE output to docs/build-log.txt
9. IF errors → fix HDL or pins; retry up to 3 times; do not claim success without 0 errors
10. IF simulation required → guide University Program VWF; LIST docs/screenshots-needed.md
11. IF program to board → Tools → Programmer, select USB-Blaster, .sof from output_files/
12. DRAFT docs/lab-report-draft.md; SYNC homework/checklist.md deliverables

---

# 6. Decision Logic（决策系统）

```
IF board unknown → ASK; never pick random device
IF DE10-Lite → device MUST be 10M50DAF484C7G MAX 10
IF compile fails → parse build-log; no fake waveforms
IF timing fails only → note in report; functional compile sufficient for most labs
IF pin Mismatch → reconcile with Terasic manual before recompile
IF lab_task vague → ask for 实验指导书 section
```

---

# 7. Tool / API Binding（工具绑定）

| Portable ID | Use | Constraints |
|-------------|-----|-------------|
| shell | | |
| file_read | | |
| file_write | | |
| ask_user | | |
| web_fetch | | |

---

# 10. Failure Modes（失败模式）

## F1: quartus-missing
- Signal: QUARTUS_NOT_FOUND
- Recovery: install Lite + device support
- Severity: block

## F2: device-mismatch
- Signal: wrong FPGA family for board
- Recovery: fix per board-devices.yaml
- Severity: block

## F3: pin-error
- Signal: illegal or conflicting pins
- Recovery: fix pin-assignment.md
- Severity: block

## F4: synthesis-error
- Signal: HDL/elaboration fail
- Recovery: fix from build-log
- Severity: block

## F5: vague-lab
- Signal: cannot infer design
- Recovery: ask handout
- Severity: block

---

# 12. Skill Graph Dependencies（依赖）

```yaml
depends_on:
  - skill-core
  - homework-assistant
provides:
  - quartus-fpga-lab
  - comp-org-lab
```

---

# 13. Versioning（版本系统）

```yaml
version: "2.0.0"
status: stable
```
