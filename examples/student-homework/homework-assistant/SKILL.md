---
name: homework-assistant
description: >-
  Unified STEM homework router: major + assignment → score unified assignment-catalog.yaml
  (FPGA, programming, MATLAB/Multisim/Keil, and planned tools for most engineering majors),
  confirm, auto-install ready lab skill(s), or run universal-stem-workflow for planned tools
  — solve "professional tools unusable in AI" via file-first assistance + install handoff.
  Use when student states 专业 + 作业. Triggers: 帮我做作业, 完成实验, 计组, Quartus, MATLAB, Simulink,
  Multisim, Keil, 单片机, Python作业, 电路仿真, 机械制图, ANSYS, 理工科实验, homework. **Single entry** —
  simulation-homework-assistant and coding-homework-assistant are aliases; always use this
  catalog.
metadata:
  version: "3.0.0"
  status: stable
  protocol: skill-protocol-v2
compatibility: install only catalog ready skills via skill-core; planned → checklist + universal-stem-workflow only
---

# Homework Assistant

## Quick Start

1. ASK major and assignment; READ refs/routing-rules.md, md-compat-index.md, stem-tool-matrix.md
2. READ refs/assignment-catalog.yaml or assignment-catalog.yaml.md; COMPUTE scores (keyword_weight, major_weight, min_score)
3. IF tie within tie_threshold → ASK pick; IF score below min_score → SHOW top 3 + ASK clarify
4. SHOW matched title, id, score, status, skills_to_install; ASK confirm before install
5. WRITE homework/session.yaml (confirmed after user OK)

## Workflow

### Step 1
ASK major and assignment; READ refs/routing-rules.md, md-compat-index.md, stem-tool-matrix.md

### Step 2
READ refs/assignment-catalog.yaml or assignment-catalog.yaml.md; COMPUTE scores (keyword_weight, major_weight, min_score)

### Step 3
IF tie within tie_threshold → ASK pick; IF score below min_score → SHOW top 3 + ASK clarify

### Step 4
SHOW matched title, id, score, status, skills_to_install; ASK confirm before install

### Step 5
WRITE homework/session.yaml (confirmed after user OK)

### Step 6
CREATE homework/{workspace_subdir}/

### Step 7
IF status planned OR skills empty → READ refs/universal-stem-workflow.md; WRITE checklist; stem-universal-fallback path; STOP (no install)

### Step 8
FIND repo_root; RESOLVE each skill per install.resolve_order (simulation-lab, coding-homework, student-homework built paths)

### Step 9
RUN install.cli_template for each skill; LOG installed_skills

### Step 10
WRITE homework/checklist.md from deliverables; ASK handout if missing

### Step 11
HANDOFF: READ installed SKILL.md; ASK lab_task for quartus-lab, python-lab, java-oop-lab, ds-algorithm-lab, ml-notebook-lab, matlab-simulink-lab, multisim-lab, keil-embedded-lab as installed

### Decision logic

```
IF user declines confirm → block install; status routing
IF install fails → retry built paths; log manual command
IF generic-fallback or stem-universal-fallback → only when no other score ≥ min_score
IF user invoked simulation-homework-assistant or coding-homework-assistant → same workflow (unified entry)
IF tool not in matrix → ASK software name; extend checklist manually
IF session exists → READ and resume unless user starts new
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
| F1 | score below min_score | top 3 + clarify + stem-tool-matrix |
| F2 | CLI error | manual command with resolve_order paths |
| F3 | tie | user choose |
| F4 | status planned or no lab skill | universal-stem-workflow; stem-universal-fallback; no fake GUI |
| F5 | user did not confirm | block install |

## Dependencies

- `skill-core`

## Additional Resources

- [IR source](references/ir.md)
