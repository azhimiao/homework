---
name: multisim-lab
profile: hybrid
status: stable
version: "1.0.0"
invocation: auto
host: any
---

# Goal
Complete NI Multisim circuit simulation lab: verify install, build circuit, run interactive sim, waveform capture, component table, report.

# Context
电路分析, 模拟电路, Multisim. After homework-assistant routes (unified catalog).

# Constraints
- 精度：multisim-setup.md; power/ground required; no fake scope shots
- 工具：check_multisim.py

# Inputs
## Required
- lab_task: string

## Optional
- multisim_path, project_path, handout

# Outputs
**Profile:** hybrid

1. `circuit.ms14` or `.ms15`
2. `docs/components.md`
3. `outputs/waveforms/`
4. `docs/report.md`

# Steps
1. READ refs/multisim-setup.md, report-template.md
2. RUN scripts/check_multisim.py; IF MULTISIM_NOT_FOUND → guide NI install; STOP
3. ASK lab_task; READ handout schematic requirements
4. GUIDE place components; WRITE docs/components.md (RefDes, value)
5. RUN interactive simulation; CAPTURE oscilloscope to outputs/waveforms/
6. VERIFY DC paths and grounds before claiming success
7. DRAFT docs/report.md per report-template; UPDATE checklist

# Decision
IF missing ground → fix before delivery
IF component values differ from handout → document in report
IF fabricated waveform → refuse F4

# Tools
- shell — check_multisim.py
- file_read, file_write, ask_user

# Failures
F1: multisim-missing | MULTISIM_NOT_FOUND | install Multisim
F2: sim-fail | circuit error | fix wiring/values
F3: vague-task | no spec | ask handout
F4: fabricated-plot | fake scope | rerun simulation

# Deps
depends_on:
  - skill-core
  - homework-assistant
provides:
  - multisim-lab

# Version
version: "1.0.0"
status: stable
