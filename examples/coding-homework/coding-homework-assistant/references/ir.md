coding-homework-assistant

---

# 0. Compilation Target

```yaml
host: any
invocation: auto
output_profile: hybrid
```

---

# 1. Intent（意图）

Theme: coding-homework

## Goal
Route programming coursework: major + assignment → score coding assignment-catalog.yaml, confirm, auto-install python-lab / java-oop-lab / ds-algorithm-lab / ml-notebook-lab, handoff with checklist.

## Context
Student says Python作业, Java实验, 数据结构, 机器学习课设. Triggers: "编程作业", "程设", "install python skill", "算法实验", "jupyter 作业".

## Constraints
- 时间：routing + install one session
- 精度：confirm before install; academic integrity — assist learn, not exam fraud
- 工具限制：skill-core install CLI; scope=project default

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

1. `homework/session.yaml`
2. `homework/checklist.md`
3. Installed lab skill(s)
4. HANDOFF with lab_task prompt

---

# 5. Execution Plan（执行流程）

1. ASK major, assignment; READ refs/routing-rules.md
2. READ refs/assignment-catalog.yaml; COMPUTE scores
3. IF tie or low score → ASK clarify or pick top 3
4. SHOW match; ASK confirm before install
5. WRITE homework/session.yaml; CREATE homework/{workspace_subdir}/
6. RESOLVE skill per install.resolve_order (coding-homework built path); install python-lab java-oop-lab ds-algorithm-lab ml-notebook-lab as matched
7. RUN skill-core install for each skill; LOG results
8. WRITE homework/checklist.md from deliverables; ASK handout
9. HANDOFF: READ installed SKILL.md; ASK lab_task; enforce academic integrity

---

# 6. Decision Logic（决策系统）

```
IF user declines confirm → block install
IF install fails → retry built path; manual command
IF ambiguous → ask choose python vs java vs ds vs ml
IF FPGA/quartus assignment → suggest student-homework homework-assistant instead
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
- Recovery: top 3 + clarify
- Severity: block

## F2: install-fail
- Signal: CLI error
- Recovery: manual command
- Severity: block

## F3: ambiguous-match
- Signal: tie
- Recovery: user choose
- Severity: block

## F4: integrity-violation
- Signal: user asks exam cheat
- Recovery: refuse; offer learning mode
- Severity: block

## F5: unconfirmed-install
- Signal: user did not confirm
- Recovery: block install
- Severity: block

---

# 12. Skill Graph Dependencies（依赖）

```yaml
depends_on:
  - skill-core
provides:
  - coding-homework-router
```

---

# 13. Versioning（版本系统）

```yaml
version: "1.0.0"
status: stable
```
