# Skill Protocol v2 — IR Reference

> **Optional spec:** [STANDARD.md](../../docs/optional/STANDARD.md)

---

## Quick index

| § | Topic | Reference |
|---|-------|-----------|
| 0 | Frontmatter bridge | §5, §20 |
| 1 | Intent | §7 |
| 2 | Inputs | §8 |
| 3 | Outputs | §9 |
| 4 | Decomposition | §10 |
| 5 | Execution Plan | §11 |
| 6 | Decision Logic | §12 |
| 7 | Tool Binding | §13 |
| 8 | Memory Model | §14 |
| 9 | Evaluation | §15 |
| 10 | Failure Modes | §16 |
| 11 | Upgrade Rules | §17 |
| 12 | Dependencies | §18 |
| 13 | Versioning | §19 |

---

## IR checklist (copy when authoring)

```
IR Progress:
- [ ] §1 Intent — Goal, Context, Constraints
- [ ] §2 Inputs — required + optional with validation
- [ ] §3 Outputs — profile declared
- [ ] §4 Decomposition — atoms pass invariant (if |steps| > 5)
- [ ] §5 Execution Plan — verb lint pass
- [ ] §6 Decision Logic — all branches terminate
- [ ] §7 Tools — portable IDs only
- [ ] §8 Memory — skill vs session distinguished
- [ ] §9 Evaluation — L0 + L1 test cases
- [ ] §10 Failures — ≥ 3 with signal + recovery
- [ ] §11 Upgrade — rules documented
- [ ] §12 Dependencies — acyclic graph
- [ ] §13 Versioning — semver + status
```

---

## Section summaries

Full detail: **protocol-v2** sections below and skill-core SKILL.md.

### §1 Intent
Goal (one sentence), Context (activation triggers), Constraints (time/cost/precision/tools).

### §2 Inputs
```yaml
- name: target_repo
  type: path
  source: author
  validation: must exist
```

### §3 Outputs
Profile: `structured` | `artifact` | `narrative` | `hybrid`

### §4 Decomposition
```yaml
id: S1
name: fetch-diff
inputs: [pr_number]
outputs: [diff_text]
primary_verb: run
```

### §5 Execution Plan
Approved verbs only. No standalone understand/analyze/think/consider.

### §6 Decision Logic
`IF <condition> → <action>` terminating in CONTINUE | STOP | RETRY | ESCALATE | FALLBACK.

### §7 Tool Binding
Portable IDs: `code_exec`, `file_read`, `file_write`, `search_code`, `web_search`, etc.  
Host mapping: [host-adapters.md](host-adapters.md)

### §8 Memory
Skill memory (files, with consent) vs session memory (this run).

### §9 Evaluation
L0 smoke → L1 task tests → L2 metrics (optional).

### §10 Failure Modes
Minimum 3: `id`, `name`, `signal`, `recovery`, `severity`.

### §11 Upgrade Rules
Evidence-gated. Version bump: patch / minor / major.

### §12 Dependencies
`depends_on`, `provides`. No cycles.

### §13 Versioning
```yaml
version: "1.0.0"
status: experimental | stable | deprecated
```

---

## Compilation contract

IR valid when skill-core Compiler Pipeline conditions hold → compile to `SKILL.md`.
