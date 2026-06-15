# Skill-Core v2 Gap Analysis

Comparison of the original v2 draft against the [Agent Skills open spec](https://agentskills.io), community skills, and production practice (2025–2026).

---

## Executive Summary

The original v2 spec is **strong as an IR (Intermediate Representation)** — it thinks like a compiler, not a wiki. Its main gaps are **runtime integration**, **progressive disclosure**, and **measurability without infrastructure**. Skill-Core closes these without diluting the 13-section model.

---

## Section-by-Section Analysis

### ✅ Strengths in Original v2

| Section | Why it works |
|---------|--------------|
| Intent | Forces clarity before writing prose |
| Inputs/Outputs | Makes skills composable and testable |
| Decomposition | Prevents "god skills" |
| Execution Plan | Action-oriented; aligns with agent strengths |
| Decision Logic | Explicit branching beats implicit LLM guessing |
| Failure Modes | Production thinking; rare in community skills |
| Upgrade Rules | Self-evolution loop; ahead of most public skills |
| Skill Graph | Enables batch development and dependency ordering |
| Versioning | Semver + status is industry standard |

### ⚠️ Gaps and Fixes

#### 1. Missing Layer 0: Frontmatter Bridge

**Gap:** Original starts with `# Skill Name` but the open spec requires YAML frontmatter with `name` and `description`. Without this, agents cannot discover or load the skill.

**Community practice:** Description is the **routing key** (~100 tokens loaded at startup for ALL skills). Must be third person, specific, include trigger terms.

**Fix:** Added §0 in protocol-v2.md + IR→Runtime mapping table in SKILL.md.

---

#### 2. Fixed JSON Output Too Rigid

**Gap:** `{ result, steps, confidence }` fits API-style skills but breaks:
- Code generation skills (output = files)
- Review skills (output = markdown feedback)
- Hybrid skills (code + explanation)

**Community practice:** Top skills (sdk, babysit, canvas) define **output shape in prose** with templates, not universal JSON.

**Fix:** Output **profiles** — `structured`, `artifact`, `narrative`, `hybrid`. JSON schema remains default for composable sub-skills only.

---

#### 3. Abstract Tool Names

**Gap:** `web_search`, `memory`, `sub_skill_call` don't map 1:1 to every host.

**Community practice:** Best skills use portable capability names; host docs list concrete tool APIs.

**Fix:** Portable tool IDs in IR + optional [host-adapters.md](host-adapters.md).

---

#### 4. Cognitive Verbs in Execution Plan

**Gap:** Original correctly bans "理解/分析" but doesn't define replacement patterns or lint rules.

**Community practice:** Best skills use imperative steps: "Run `gh pr create`", "Read git status", "If X, ask user".

**Fix:** Verb lint table + approved verb list + atom invariant formula.

---

#### 5. No Progressive Disclosure

**Gap:** 13 sections in one SKILL.md easily exceeds 500 lines / 5000 tokens — the #1 community anti-pattern ("wiki skill").

**Community practice:** agentskills.io recommends metadata → SKILL.md → references/ on demand. Cursor create-skill skill enforces <500 lines.

**Fix:** IR lives in `references/` or draft; runtime SKILL.md is compiled subset. Heavy eval/memory in separate files.

---

#### 6. Evaluation Metrics Without Baselines

**Gap:** `success_rate > 0.8` requires telemetry that doesn't exist for most personal skills.

**Community practice:** Mature skills use **verification steps** (run test, check output) not dashboards.

**Fix:** Tiered evaluation L0 (smoke) → L1 (task tests) → L2 (metrics). Upgrade rules gated on L2 evidence.

---

#### 7. Memory Model Over-Promises

**Gap:** `{ episodic, patterns, failures }` implies persistent agent memory. Most agents lack cross-session episodic storage by default.

**Community practice:** "Memory" = project rules, reference files, conversation context. Writes need explicit user consent.

**Fix:** Split **skill memory** (file-backed references) vs **session memory** (this run). No fake persistence.

---

#### 8. No Verbatim Preservation Rule

**Gap:** When users provide exact skill text, agents paraphrase and lose intent.

**Community practice:** Mature authoring workflows mandate verbatim copy when the skill author supplies exact text.

**Fix:** Explicit rule in Compiler Pipeline Phase 0.

---

#### 9. Meta-Skill Discovery Pollution

**Gap:** A skill that "builds all skills" would auto-trigger on every skill-related mention, wasting context.

**Community practice:** Meta/tooling skills use `disable-model-invocation: true` (create-skill default).

**Fix:** skill-core sets `disable-model-invocation: true`; invoke via `/skill-core`.

---

#### 10. Missing Anti-Patterns and Validation

**Gap:** Protocol defines what TO do, not what NOT to do.

**Community practice:** create-skill has extensive anti-patterns (Windows paths, too many options, time-sensitive info).

**Fix:** Anti-pattern section + validate_skill.py script.

---

#### 11. No Compiler Workflow

**Gap:** IR concept stated but no steps from Intent → deployed skill.

**Fix:** 6-phase Compiler Pipeline with checklist.

---

#### 12. Skill Graph Without Cycle Detection

**Gap:** `depends_on` can create circular dependencies in batch builds.

**Fix:** Batch development section + validation rule: no circular deps; create leaves first.

---

## Comparison Matrix

| Dimension | Typical Community Skill | Original v2 | Skill-Core v2 |
|-----------|------------------------|-------------|---------------|
| Discovery | Good description | Missing frontmatter | Frontmatter + IR map |
| Structure | Freeform markdown | 13-section IR | IR + compiled runtime |
| Outputs | Templates/prose | Fixed JSON | 4 profiles |
| Tools | Named implicitly | Abstract names | Portable IDs + host adapters |
| Size | Often too long | Would be too long | Progressive disclosure |
| Testing | Manual | Metrics only | L0/L1/L2 tiers |
| Evolution | None | Upgrade rules | Gated on evidence |
| Batch | Ad hoc | Graph deps | Full batch workflow |

---

## What We Deliberately Did NOT Add

To avoid over-engineering:

- **No custom DSL parser** — markdown IR is enough; Python validator is optional
- **No mandatory JSON for all skills** — profiles cover real use cases
- **No fake telemetry** — L2 metrics optional until infrastructure exists
- **No duplicate onboarding docs** — skill-core is protocol + compiler; host-specific setup stays in host-adapters.md

---

## Recommended Reading Order

1. skill-core/SKILL.md — operational compiler
2. references/protocol-v2.md — full IR when designing
3. references/template.skill.md — copy to start new skill
4. references/example-compiled.md — see IR → runtime transform
