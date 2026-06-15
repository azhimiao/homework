# Skill Name
<!-- IR only — compile to SKILL.md via skill-core -->

<skill-name>

---

# 0. Compilation Target

```yaml
deploy_to: skills/<skill-name>/
host: any  # or cursor | claude-code | custom
```

---

# 1. Intent（意图）

## Goal
<这个 skill 要解决什么问题 — one sentence outcome>

## Context
<使用场景 — user phrases, file types, when agent should activate>

## Constraints
- 时间：<e.g. single session, < 5 min>
- 成本：<e.g. minimal API calls>
- 精度：<e.g. exact | best-effort | human review>
- 工具限制：<e.g. read-only, no network>

---

# 2. Inputs（输入定义）

## Required Inputs
- input_1: <type> — <description> — validation: <rule>
- input_2: <type> — <description> — validation: <rule>

## Optional Inputs
- input_x: <type> — default: <value>

---

# 3. Outputs（输出定义）

**Profile:** structured | artifact | narrative | hybrid

```json
{
  "result": "",
  "steps": [],
  "confidence": 0.0,
  "errors": []
}
```

---

# 4. Skill Decomposition（能力拆解）

## S1: <name>
- Goal:
- Inputs:
- Outputs:
- Primary verb:

## S2: <name>
- Goal:
- Inputs:
- Outputs:
- Primary verb:

## S3: <name>
- Goal:
- Inputs:
- Outputs:
- Primary verb:

---

# 5. Execution Plan（执行流程）

1. READ …
2. RUN …
3. TRANSFORM …
4. VALIDATE …
5. GENERATE …

<!-- Every step must use approved action verbs. No standalone "理解/分析". -->

---

# 6. Decision Logic（决策系统）

```
IF <condition A> → <action B>
IF <failure> → <fallback C>
IF confidence < 0.4 → RE-RUN S2
IF <missing input> → ASK user
```

---

# 7. Tool / API Binding（工具绑定）

| Portable ID | Use | Constraints |
|-------------|-----|-------------|
| file_read | | |
| code_exec | | |
| file_write | | |
| sub_skill_call | | |

Host mapping: skill-core `references/host-adapters.md`.

---

# 8. Memory Model（记忆结构）

## Skill memory (file-backed)
```json
{
  "patterns": [],
  "failures": [],
  "decisions": []
}
```

## Session memory
<what to carry from step N to step N+1 this run>

---

# 9. Evaluation（评估标准）

## L0 Smoke
- [ ] Happy path completes
- [ ] Frontmatter will be valid

## L1 Task (before stable)
See `references/eval.yaml` for automated L1 tests.

## L2 Metrics (optional)

---

# 10. Failure Modes（失败模式）

## F1: <name>
- Signal:
- Recovery:
- Severity: block | degrade

## F2: <name>
- Signal:
- Recovery:
- Severity:

## F3: <name>
- Signal:
- Recovery:
- Severity:

---

# 11. Upgrade Rules（自进化规则）

```
IF success_rate > 0.8 → abstract shared steps to sub-skill
IF failure repeats ≥3 → split skill or add branch
IF latency high → compress steps / add script
IF ambiguity high → refine inputs / add examples
```

---

# 12. Skill Graph Dependencies（依赖）

```yaml
depends_on:
  - skill-core
provides:
  - <capability-this-skill-exposes>
```

---

# 13. Versioning（版本系统）

```yaml
version: "0.1.0"
parent: none
status: experimental
changelog:
  - "0.1.0: initial IR"
```
