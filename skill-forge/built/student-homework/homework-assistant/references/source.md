---
name: homework-assistant
profile: hybrid
status: stable
version: "3.0.0"
invocation: auto
host: any
---

# Goal
Unified STEM homework router: major + assignment → score unified assignment-catalog.yaml (FPGA, programming, MATLAB/Multisim/Keil, and planned tools for most engineering majors), confirm, auto-install ready lab skill(s), or run universal-stem-workflow for planned tools — solve "professional tools unusable in AI" via file-first assistance + install handoff.

# Context
Student states 专业 + 作业. Triggers: 帮我做作业, 完成实验, 计组, Quartus, MATLAB, Simulink, Multisim, Keil, 单片机, Python作业, 电路仿真, 机械制图, ANSYS, 理工科实验, homework. **Single entry** — simulation-homework-assistant and coding-homework-assistant are aliases; always use this catalog.

# Constraints
- 时间：routing + install one session; lab continues in installed skill
- 精度：confirm before install; no fabricated compile/simulation results
- 工具限制：install only catalog ready skills via skill-core; planned → checklist + universal-stem-workflow only
- 学术诚信：assist learning; refuse exam fraud

# Inputs
## Required
- major: string
- assignment: string

## Optional
- project_dir, host, scope, handout

# Outputs
**Profile:** hybrid

1. `homework/session.yaml`
2. `homework/checklist.md`
3. Installed lab skill(s) when status ready
4. HANDOFF with lab_task or universal workflow steps

# Steps
1. ASK major and assignment; READ refs/routing-rules.md, md-compat-index.md, stem-tool-matrix.md
2. READ refs/assignment-catalog.yaml or assignment-catalog.yaml.md; COMPUTE scores (keyword_weight, major_weight, min_score)
3. IF tie within tie_threshold → ASK pick; IF score below min_score → SHOW top 3 + ASK clarify
4. SHOW matched title, id, score, status, skills_to_install; ASK confirm before install
5. WRITE homework/session.yaml (confirmed after user OK)
6. CREATE homework/{workspace_subdir}/
7. IF status planned OR skills empty → READ refs/universal-stem-workflow.md; WRITE checklist; stem-universal-fallback path; STOP (no install)
8. FIND repo_root; RESOLVE each skill per install.resolve_order (simulation-lab, coding-homework, student-homework built paths)
9. RUN install.cli_template for each skill; LOG installed_skills
10. WRITE homework/checklist.md from deliverables; ASK handout if missing
11. HANDOFF: READ installed SKILL.md; ASK lab_task for quartus-lab, python-lab, java-oop-lab, ds-algorithm-lab, ml-notebook-lab, matlab-simulink-lab, multisim-lab, keil-embedded-lab as installed

# Decision
IF user declines confirm → block install; status routing
IF install fails → retry built paths; log manual command
IF generic-fallback or stem-universal-fallback → only when no other score ≥ min_score
IF user invoked simulation-homework-assistant or coding-homework-assistant → same workflow (unified entry)
IF tool not in matrix → ASK software name; extend checklist manually
IF session exists → READ and resume unless user starts new

# Tools
- ask_user, file_read, file_write, shell, memory_read

# Failures
F1: no-match | score below min_score | top 3 + clarify + stem-tool-matrix
F2: install-fail | CLI error | manual command with resolve_order paths
F3: ambiguous-match | tie | user choose
F4: planned-tool | status planned or no lab skill | universal-stem-workflow; stem-universal-fallback; no fake GUI
F5: unconfirmed-install | user did not confirm | block install
F6: integrity-violation | exam cheat request | refuse; learning mode

# Deps
depends_on:
  - skill-core
provides:
  - homework-router
  - stem-homework-router
  - skill-auto-install

# Version
version: "3.0.0"
status: stable
