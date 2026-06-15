---
name: matlab-simulink-lab
profile: hybrid
status: stable
version: "1.0.0"
invocation: auto
host: any
---

# Goal
Complete MATLAB/Simulink control or signal labs: verify MATLAB, build .m/.slx, run simulation, capture plots, params doc, report per report-template.md.

# Context
After homework-assistant routes (unified STEM catalog). Triggers: 自动控制原理, Simulink, 阶跃响应, PID.

# Constraints
- 精度：matlab-simulink-setup.md; document K,T,PID; no fake plots
- 工具：check_matlab.py first

# Inputs
## Required
- lab_task: string

## Optional
- matlab_path, project_path, use_simulink: boolean, handout

# Outputs
**Profile:** hybrid

1. `scripts/*.m`, `models/*.slx` if needed
2. `docs/params.md`, `outputs/figures/`
3. `docs/report.md` six-section

# Steps
1. READ refs/matlab-simulink-setup.md, report-template.md
2. RUN scripts/check_matlab.py; IF MATLAB_NOT_FOUND → guide install; STOP
3. ASK lab_task; READ handout
4. CREATE project under homework/matlab-lab/
5. IMPLEMENT .m or .slx; RECORD params in docs/params.md
6. RUN simulation; SAVE figures to outputs/figures/
7. IF Simulink → verify solver settings match handout
8. DRAFT docs/report.md; UPDATE checklist

# Decision
IF lab_task vague → ASK handout
IF simulation diverges from theory → note in analysis section
IF user claims results without run → refuse fabricated plots

# Tools
- shell — matlab -batch
- file_read, file_write, ask_user

# Failures
F1: matlab-missing | MATLAB_NOT_FOUND | install MATLAB
F2: sim-error | model does not run | fix equations/blocks
F3: vague-task | no spec | ask handout
F4: fabricated-plot | no run claimed | rerun and capture

# Deps
depends_on:
  - skill-core
  - homework-assistant
provides:
  - matlab-simulink-lab

# Version
version: "1.0.0"
status: stable
