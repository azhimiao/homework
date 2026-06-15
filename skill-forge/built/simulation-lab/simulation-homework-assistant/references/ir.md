simulation-homework-assistant

---

# 0. Compilation Target

```yaml
host: any
invocation: auto
output_profile: hybrid
```

---

# 1. Intent（意图）

Theme: simulation-lab

## Goal
Alias of homework-assistant for simulation triggers (MATLAB, Simulink, Multisim, Keil). **Delegate entirely** to homework-assistant v3 unified catalog — same confirm → install → handoff; no separate simulation-lab catalog.

## Context
Triggers: MATLAB实验, Simulink, Multisim, 电路仿真, Keil, 单片机实验, 自动控制实验. User may install this skill or homework-assistant; behavior identical.

## Constraints
- 精度：confirm before install; real simulation before claim success
- 路由：READ student-homework refs/assignment-catalog.yaml only

---

# 2. Inputs（输入定义）

## Required Inputs
## Required
- major: string
- assignment: string

## Optional
- project_dir, host, scope, handout

---

# 3. Outputs（输出定义）

**Profile:** hybrid

Same as homework-assistant: session.yaml, checklist.md, installed lab skill(s), HANDOFF.

---

# 5. Execution Plan（执行流程）

1. DELEGATE to homework-assistant workflow (Steps 1–11); WRITE homework/session.yaml
2. READ student-homework refs/assignment-catalog.yaml, routing-rules.md, stem-tool-matrix.md
3. MATCH matlab-control-lab, multisim-circuit-lab, keil-embedded-lab or planned spice/proteus/labview entries
4. CONFIRM → install matlab-simulink-lab, multisim-lab, keil-embedded-lab via resolve_order (simulation-lab built path)
5. WRITE homework/checklist.md; HANDOFF to installed lab skill with lab_task

---

# 6. Decision Logic（决策系统）

```
IF user declines confirm → block install
IF FPGA/quartus → same catalog routes comp-org-quartus → quartus-lab
IF pure coding → same catalog routes python/java/ds/ml labs
IF install fails → manual command with skill-forge/built/simulation-lab path
IF planned-tool match → universal-stem-workflow; no install
```

---

# 7. Tool / API Binding（工具绑定）

| Portable ID | Use | Constraints |
|-------------|-----|-------------|
| ask_user, | | |

---

# 10. Failure Modes（失败模式）

## F1: no-match
- Signal: score below min_score
- Recovery: stem-tool-matrix + clarify
- Severity: block

## F2: install-fail
- Signal: CLI error
- Recovery: manual command
- Severity: block

## F3: ambiguous-match
- Signal: tie
- Recovery: user choose
- Severity: block

## F4: unconfirmed-install
- Signal: user did not confirm
- Recovery: block install
- Severity: block

## F5: planned-tool
- Signal: ltspice proteus labview planned
- Recovery: universal-stem-workflow; no install
- Severity: block

---

# 12. Skill Graph Dependencies（依赖）

```yaml
depends_on:
  - skill-core
  - homework-assistant
provides:
  - simulation-homework-router
```

---

# 13. Versioning（版本系统）

```yaml
version: "2.0.0"
status: stable
```
