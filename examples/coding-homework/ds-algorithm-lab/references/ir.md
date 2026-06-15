ds-algorithm-lab

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
Complete data structures / algorithms lab: implement algorithm, complexity analysis, tests, report.

## Context
数据结构实验, 算法作业, 链表/树/图. Triggers: "数据结构", "算法实验", "复杂度".

## Constraints
- 精度：ds-algorithms-guide.md; complexity doc required
- 语言：default Python unless handout specifies

---

# 2. Inputs（输入定义）

## Required Inputs
## Required
- lab_task: string — e.g. 实现快速排序并分析复杂度

## Optional
- language: python | java, project_path, handout

---

# 3. Outputs（输出定义）

**Profile:** hybrid

1. `src/` implementation
2. `tests/` with cases
3. `docs/complexity.md`
4. `docs/report.md`

---

# 5. Execution Plan（执行流程）

1. READ refs/ds-algorithms-guide.md
2. RUN check_python.py if Python else check_java.py
3. ASK lab_task and algorithm spec; READ handout
4. IMPLEMENT with clear API; WRITE tests
5. RUN pytest or handout cases; all pass
6. WRITE docs/complexity.md — O time/space
7. DRAFT report; UPDATE checklist

---

# 6. Decision Logic（决策系统）

```
IF handout gives Java → switch toolchain
IF wrong complexity → revise before delivery
IF only paste LeetCode without local run → require local tests
```

---

# 7. Tool / API Binding（工具绑定）

| Portable ID | Use | Constraints |
|-------------|-----|-------------|
| shell, | | |

---

# 10. Failure Modes（失败模式）

## F1: toolchain-missing
- Signal: no python/java
- Recovery: install
- Severity: block

## F2: test-fail
- Signal: cases fail
- Recovery: fix algorithm
- Severity: block

## F3: missing-complexity
- Signal: no O() doc
- Recovery: add complexity.md
- Severity: block

## F4: integrity-violation
- Signal: cheat
- Recovery: refuse
- Severity: block

---

# 12. Skill Graph Dependencies（依赖）

```yaml
depends_on:
  - skill-core
  - coding-homework-assistant
provides:
  - ds-algorithm-lab
```

---

# 13. Versioning（版本系统）

```yaml
version: "1.0.0"
status: stable
```
