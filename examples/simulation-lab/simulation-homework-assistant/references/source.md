---
name: simulation-homework-assistant
profile: hybrid
status: stable
version: "2.0.0"
invocation: auto
host: any
---

# Goal
Alias of homework-assistant for simulation triggers (MATLAB, Simulink, Multisim, Keil). **Delegate entirely** to homework-assistant v3 unified catalog — same confirm → install → handoff; no separate simulation-lab catalog.

# Context
Triggers: MATLAB实验, Simulink, Multisim, 电路仿真, Keil, 单片机实验, 自动控制实验. User may install this skill or homework-assistant; behavior identical.

# Constraints
- 精度：confirm before install; real simulation before claim success
- 路由：READ student-homework refs/assignment-catalog.yaml only

# Inputs
## Required
- major: string
- assignment: string

## Optional
- project_dir, host, scope, handout

# Outputs
**Profile:** hybrid

Same as homework-assistant: session.yaml, checklist.md, installed lab skill(s), HANDOFF.

# Steps
1. DELEGATE to homework-assistant workflow (Steps 1–11); WRITE homework/session.yaml
2. READ student-homework refs/assignment-catalog.yaml, routing-rules.md, stem-tool-matrix.md
3. MATCH matlab-control-lab, multisim-circuit-lab, keil-embedded-lab or planned spice/proteus/labview entries
4. CONFIRM → install matlab-simulink-lab, multisim-lab, keil-embedded-lab via resolve_order (simulation-lab built path)
5. WRITE homework/checklist.md; HANDOFF to installed lab skill with lab_task

# Decision
IF user declines confirm → block install
IF FPGA/quartus → same catalog routes comp-org-quartus → quartus-lab
IF pure coding → same catalog routes python/java/ds/ml labs
IF install fails → manual command with skill-forge/built/simulation-lab path
IF planned-tool match → universal-stem-workflow; no install

# Tools
- ask_user, file_read, file_write, shell, memory_read

# Failures
F1: no-match | score below min_score | stem-tool-matrix + clarify
F2: install-fail | CLI error | manual command
F3: ambiguous-match | tie | user choose
F4: unconfirmed-install | user did not confirm | block install
F5: planned-tool | ltspice proteus labview planned | universal-stem-workflow; no install

# Deps
depends_on:
  - skill-core
  - homework-assistant
provides:
  - simulation-homework-router

# Version
version: "2.0.0"
status: stable
