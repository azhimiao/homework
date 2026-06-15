---
name: quartus-lab
profile: hybrid
status: stable
version: "2.0.0"
invocation: auto
host: any
---

# Goal
Accurate Intel Quartus Prime lab workflow: detect toolchain, select correct MAX10/Cyclone device per board, assign pins from board manual, compile, program, simulate, draft report.

# Context
After homework-assistant routes 计组/FPGA work, or direct Quartus request. Triggers: "Quartus", "计组实验", "FPGA", "Verilog", "DE10-Lite", "引脚", "Programmer".

# Constraints
- 时间：one lab focus per session
- 精度：device from board-devices.yaml; pins from board-pins/*.md or Terasic manual — never guess
- 工具限制：run check_quartus.py first; no fabricated compile success

# Inputs
## Required
- lab_task: string — 实验要求（如 ALU、交通灯、计数器）

## Optional
- board: string — DE10-Lite | DE1-SoC | DE2-115 | DE10-Standard | DE0-CV — default from catalog default_board or ASK
- language: enum — verilog | vhdl | bdf — default: verilog
- project_path: path — default: homework/comp-org-lab/{project_name}/
- quartus_path: path — from check_quartus.py if not on PATH

# Outputs
**Profile:** hybrid

1. Quartus project (.qpf, .qsf, src/*.v)
2. `docs/pin-assignment.md` — signal → PIN table
3. `docs/build-log.txt` — compile output
4. `docs/lab-report-draft.md` — 六段报告草稿
5. `docs/screenshots-needed.md` — RTL / waveform / Programmer 清单

# Steps
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

# Decision
IF board unknown → ASK; never pick random device
IF DE10-Lite → device MUST be 10M50DAF484C7G MAX 10
IF compile fails → parse build-log; no fake waveforms
IF timing fails only → note in report; functional compile sufficient for most labs
IF pin Mismatch → reconcile with Terasic manual before recompile
IF lab_task vague → ask for 实验指导书 section

# Tools
- shell — check_quartus.py, quartus_sh --flow compile
- file_read — board-devices.yaml, board-pins, handout, qsf
- file_write — src, docs/*, qsf pin assignments
- ask_user — board, lab number, handout, upload screenshot confirm
- web_fetch — Terasic manual URL if user provides

# Failures
F1: quartus-missing | QUARTUS_NOT_FOUND | install Lite + device support
F2: device-mismatch | wrong FPGA family for board | fix per board-devices.yaml
F3: pin-error | illegal or conflicting pins | fix pin-assignment.md
F4: synthesis-error | HDL/elaboration fail | fix from build-log
F5: vague-lab | cannot infer design | ask handout

# Deps
depends_on:
  - skill-core
  - homework-assistant
provides:
  - quartus-fpga-lab
  - comp-org-lab

# Version
version: "2.0.0"
status: stable
