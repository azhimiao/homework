---
name: coding-homework-assistant
profile: hybrid
status: stable
version: "1.0.0"
invocation: auto
host: any
---

# Goal
Route programming coursework: major + assignment → score coding assignment-catalog.yaml, confirm, auto-install python-lab / java-oop-lab / ds-algorithm-lab / ml-notebook-lab, handoff with checklist.

# Context
Student says Python作业, Java实验, 数据结构, 机器学习课设. Triggers: "编程作业", "程设", "install python skill", "算法实验", "jupyter 作业".

# Constraints
- 时间：routing + install one session
- 精度：confirm before install; academic integrity — assist learn, not exam fraud
- 工具限制：skill-core install CLI; scope=project default

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
3. Installed lab skill(s)
4. HANDOFF with lab_task prompt

# Steps
1. ASK major, assignment; READ refs/routing-rules.md
2. READ refs/assignment-catalog.yaml; COMPUTE scores
3. IF tie or low score → ASK clarify or pick top 3
4. SHOW match; ASK confirm before install
5. WRITE homework/session.yaml; CREATE homework/{workspace_subdir}/
6. RESOLVE skill per install.resolve_order (coding-homework built path); install python-lab java-oop-lab ds-algorithm-lab ml-notebook-lab as matched
7. RUN skill-core install for each skill; LOG results
8. WRITE homework/checklist.md from deliverables; ASK handout
9. HANDOFF: READ installed SKILL.md; ASK lab_task; enforce academic integrity

# Decision
IF user declines confirm → block install
IF install fails → retry built path; manual command
IF ambiguous → ask choose python vs java vs ds vs ml
IF FPGA/quartus assignment → suggest student-homework homework-assistant instead

# Tools
- ask_user, file_read, file_write, shell, memory_read

# Failures
F1: no-match | score below min_score | top 3 + clarify
F2: install-fail | CLI error | manual command
F3: ambiguous-match | tie | user choose
F4: integrity-violation | user asks exam cheat | refuse; offer learning mode
F5: unconfirmed-install | user did not confirm | block install

# Deps
depends_on:
  - skill-core
provides:
  - coding-homework-router

# Version
version: "1.0.0"
status: stable
