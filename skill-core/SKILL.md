---
name: skill-core
description: >-
  Skill Protocol v2 compiler and meta-skill for building Agent Skills at scale.
  Defines the standardized IR, scaffolds new skills, validates compliance, and
  guides decomposition and evolution. Use when creating any skill, batch-developing
  skills, reviewing SKILL.md structure, Skill Protocol v2, or skill-core.
disable-model-invocation: true
metadata:
  version: "2.0.0"
  protocol-version: "2.0"
  protocol: skill-protocol-v2
  role: meta-skill
  status: stable
  extends: agentskills.io
compatibility: Agent Skills open standard. Requires file write access for scaffolding.
---

# Skill-Core

**Skill-Core is the Skill Protocol compiler** — the unified contract every Agent Skill must follow, plus the workflow to produce compliant skills at scale.

This is a **developer product**: it helps you design, compile, validate, and ship skills for any Agent Skills-compatible host. It is not tied to a single IDE or vendor.

```
Intent → IR (13 sections) → SKILL.md (runtime) → Agent Host → Eval → Upgrade
```

Start here when creating, reviewing, splitting, or evolving a skill. Load `references/` only when needed.

**Optional spec:** [STANDARD.md](../docs/optional/STANDARD.md)  
**New to Agent Skills?** [what-is-agent-skill.md](references/what-is-agent-skill.md)

---

## When to Apply

| Trigger | Action |
|---------|--------|
| "Create a skill for X" | Run **Compiler Pipeline** (below) |
| "Review this skill" | Run **Validation Checklist** |
| "Batch create skills" | Repeat pipeline per skill; share `depends_on` graph |
| "What's wrong with this skill?" | Compare against [protocol-v2.md](references/protocol-v2.md) |
| User provides verbatim skill text | Copy **verbatim** into IR/outputs — do not paraphrase |

---

## Architecture: Two Layers

| Layer | File | Purpose |
|-------|------|---------|
| **IR** (Intermediate Representation) | `references/template.skill.md` or draft in chat | Full 13-section protocol; design-time |
| **Runtime** (Agent Skills spec) | `SKILL.md` in skill folder | Open-standard frontmatter + executable body; load-time |

**Rule:** IR is the source of truth during design. Runtime `SKILL.md` is the compiled artifact the agent loads. Never skip IR for non-trivial skills — it prevents vague instructions from reaching production.

### IR → Runtime Mapping

| IR Section | Runtime Location |
|------------|------------------|
| Skill Name | YAML `name` (must match folder name) |
| Intent.Goal + Context | YAML `description` (third person, WHAT + WHEN) |
| Constraints (tools/env) | YAML `compatibility`, `allowed-tools` |
| Versioning | YAML `metadata.version`, `metadata.status` |
| Tool Binding | Body § Tools + `scripts/` |
| Execution Plan | Body § Workflow (imperative steps) |
| Decision Logic | Body § Decision tree |
| Outputs | Body § Output format + `assets/` templates |
| Decomposition | Separate skill folders + `depends_on` |
| Evaluation / Failure / Upgrade | Body § Verification + `references/eval.md` if heavy |
| Memory Model | `references/memory.md` or project memory rules |
| Full IR detail | `references/protocol-v2.md` (progressive disclosure) |

---

## Gap Analysis: v2 Original vs Production-Ready

The v2 IR draft is strong compiler thinking. These gaps were closed in Skill-Core:

| Gap | Problem | Fix |
|-----|---------|-----|
| No frontmatter bridge | Agent Skills spec requires `name` + `description` | Layer 0 frontmatter + mapping table above |
| Fixed JSON output | Many skills produce files, code, or narrative | Output **profiles**: `structured`, `artifact`, `narrative`, `hybrid` |
| Abstract tool names | IR names don't map 1:1 to every host | **Portable tool IDs** + optional [host-adapters.md](references/host-adapters.md) |
| "Understand/analyze" in steps | Non-executable | **Verb lint**: steps must start with action verbs |
| 13 sections in one file | Blows 500-line / 5000-token budget | Progressive disclosure: IR in `references/` |
| Metrics without baselines | `success_rate > 0.8` unusable without data | Tiered eval: **L0 smoke** → **L1 task** → **L2 metrics** |
| Memory model aspirational | Agents lack cross-session episodic store by default | Distinguish **skill memory** (files) vs **session memory** (this run) |
| No verbatim rule | Author copy gets rewritten | Explicit verbatim preservation rule |
| No anti-patterns | Same mistakes repeat | Anti-pattern list in protocol |
| Meta-skill auto-fires | Pollutes unrelated sessions | `disable-model-invocation: true` on skill-core |

Full analysis: [gap-analysis.md](references/gap-analysis.md)

---

## Compiler Pipeline

Copy this checklist and track progress when building any skill:

```
Skill Build Progress:
- [ ] Phase 0: Intent captured
- [ ] Phase 1: IR drafted (13 sections)
- [ ] Phase 2: IR reviewed (verb lint + atom check)
- [ ] Phase 3: Compiled to SKILL.md
- [ ] Phase 4: Supporting files (scripts/references/assets)
- [ ] Phase 5: Validated
- [ ] Phase 6: Deployed
```

### Phase 0: Intent Capture

Ask or infer:

1. **Goal** — one sentence, outcome-focused
2. **Context** — when should an agent activate this skill?
3. **Constraints** — time, cost, precision, tool limits
4. **Target location** — dev repo (e.g. `skills/<name>/`) → host install path (see Deploy)
5. **Invocation mode** — auto-apply vs manual (`disable-model-invocation` where supported)

If the author provided exact skill text, mark it `verbatim: true` and preserve it.

### Phase 1: Draft IR

Start from [template.skill.md](references/template.skill.md). Fill all 13 sections.

Minimum quality gates before compile:

- **S1–Sn decomposition**: each sub-skill has named inputs, named outputs, one primary action verb
- **Execution plan**: every step passes verb lint (see below)
- **Decision logic**: every branch has a concrete action, not "handle appropriately"
- **Failure modes**: at least 3, each with detection signal + recovery action
- **Outputs**: pick a profile and define schema or template

### Phase 2: IR Review

**Verb lint** — REJECT steps containing only cognitive verbs without a concrete action:

| Banned alone | Replace with |
|--------------|----------------|
| understand | read `<file>`, query `<source>`, list `<fields>` |
| analyze | run `<script>`, diff `<A>` vs `<B>`, count `<metric>` |
| think about | compare `<X>` to `<Y>`, check `<invariant>` |
| consider | if `<cond>` then run `<action>` else run `<fallback>` |

**Atom check** — each sub-skill must satisfy:

```
ATOM(S) := has_input(S) ∧ has_output(S) ∧ has_executable_step(S) ∧ ¬uses_abstract_verb_only(S)
```

### Phase 3: Compile to Runtime SKILL.md

Transform IR into this runtime structure:

```markdown
---
name: <folder-name>
description: <third-person WHAT + WHEN, ≤1024 chars, trigger keywords>
disable-model-invocation: <true|false>
metadata:
  version: "<semver>"
  status: experimental|stable|deprecated
  protocol: "skill-protocol-v2"
compatibility: <if needed>
---

# <Human Title>

## Quick Start
<3–5 imperative steps from Execution Plan>

## Workflow
<full step-by-step from §5 + §6>

## Inputs / Outputs
<from §2 + §3, condensed>

## Tools
<from §7 — portable tool IDs; see host-adapters.md if needed>

## Verification
<from §9 + §10: how to know it worked>

## Sub-skills
<from §4, if any>

## Additional Resources
- [protocol-v2.md](references/protocol-v2.md) — only for maintainers
```

Keep runtime `SKILL.md` **under 500 lines**. Move heavy content to `references/`.

### Phase 4: Supporting Files

Standard layout:

```
skill-name/
├── SKILL.md
├── references/       # IR detail, eval rubrics, domain docs
├── scripts/          # repeatable, fragile, or deterministic ops
└── assets/           # templates, schemas, static outputs
```

Use `scripts/` when the operation is **repeatable and fragile** (validation, scaffolding, API calls with fixed shape). Use `references/` for **read-on-demand** detail.

### Phase 5: Validate

Run:

```bash
python scripts/validate_skill.py ./skill-name
```

Or manually run **Validation Checklist** (below).

### Phase 6: Deploy

Install compiled skill to a host that supports the [Agent Skills spec](https://agentskills.io):

| Scope | Common paths (pick your host) |
|-------|-------------------------------|
| Dev / source repo | `skills/<name>/` or monorepo `packages/skills/<name>/` |
| Project (team-shared) | `.agents/skills/<name>/` · `.cursor/skills/<name>/` |
| Personal (global) | `~/.cursor/skills/<name>/` · `~/.claude/skills/<name>/` |

Do not overwrite vendor-shipped built-in skill directories. Use your own `skills/` or `.agents/skills/` tree.

See [host-adapters.md](references/host-adapters.md) for per-host path and tool notes.

---

## Output Profiles (§3 Enhancement)

Not every skill emits JSON. Pick one:

| Profile | When | Shape |
|---------|------|-------|
| `structured` | Tool/API pipelines, composable sub-skills | JSON with `result`, `steps`, `confidence` |
| `artifact` | File/code/template generation | `{ "artifacts": [{ "path", "type" }], "summary" }` |
| `narrative` | Reviews, explanations, decisions | Markdown sections with required headings |
| `hybrid` | Code + explanation | Artifact list + narrative summary |

Default for composable/sub-skills: `structured`. Default for user-facing deliverables: `artifact` or `narrative`.

---

## Tool Binding Registry (§7 — Portable)

Define tools in IR using **portable IDs**. Host-specific names live in [host-adapters.md](references/host-adapters.md).

| Portable ID | Capability | Typical use |
|-------------|------------|-------------|
| `web_search` | Search the public web | docs, APIs, errors |
| `web_fetch` | Fetch URL content | specs, changelogs |
| `code_exec` | Run shell/commands | tests, git, build |
| `file_read` | Read files | source, config |
| `file_write` | Write or patch files | codegen, edits |
| `search_code` | Search repository | symbols, patterns |
| `sub_skill_call` | Invoke another skill | composition |
| `subagent` | Delegate to sub-agent | parallel work |
| `memory_read` | Read persisted notes | patterns, prior fixes |
| `memory_write` | Append learning notes | post-mortems (with consent) |
| `ask_user` | Clarify with author | missing inputs |

Document allowed tools in IR §7. Use frontmatter `allowed-tools` when the spec supports restricting scope.

---

## Evaluation Tiers (§9 Enhancement)

| Tier | When | Criteria |
|------|------|----------|
| **L0 Smoke** | Every skill at creation | Frontmatter valid; ≥1 executable step; outputs defined; 3 failure modes |
| **L1 Task** | Before marking `stable` | 3 manual test cases pass; decision branches covered |
| **L2 Metrics** | Mature / automated skills | Quantify: `success_rate`, `accuracy`, `latency_p95`, `reuse_rate` |

Upgrade rules (§11) apply **after L2 baselines exist**. Until then, use L1 qualitative signals.

---

## Validation Checklist

### Frontmatter
- [ ] `name` matches folder; lowercase, hyphens, ≤64 chars
- [ ] `description` is third person, includes WHAT + WHEN + trigger terms
- [ ] `metadata.version` and `metadata.status` set

### Body
- [ ] Quick Start exists (≤5 steps)
- [ ] All workflow steps pass verb lint
- [ ] Inputs and outputs defined with profile
- [ ] ≥3 failure modes with recovery
- [ ] File refs one level deep; forward slashes only
- [ ] SKILL.md < 500 lines

### Ecosystem
- [ ] `depends_on` skills exist or are created in same batch
- [ ] No circular dependencies in skill graph
- [ ] Scripts run without undeclared deps

---

## Batch Skill Development

When building multiple skills in your dev repo:

1. **Inventory** — list skills with one-line Goal
2. **Graph first** — draw `depends_on`; create leaf skills before dependents
3. **Shared assets** — extract common patterns into `skill-core/references/` or a shared `lib/` skill
4. **Parallel IR** — draft IR for independent skills in parallel
5. **Serial compile** — compile and validate one at a time
6. **Integration pass** — verify cross-skill calls and graph

---

## Skill Evolution (§11)

After deployment, apply upgrade rules when evidence exists:

| Signal | Action |
|--------|--------|
| L2 `success_rate > 0.8` over ≥20 runs | Abstract shared steps into new sub-skill |
| Same failure mode ≥3 times | Split skill or add explicit decision branch |
| L2 `latency_p95` above budget | Compress steps; move detail to `references/`; add script |
| High input ambiguity (clarification rate > 30%) | Refine §2 Required Inputs; add examples |
| Skill triggers incorrectly | Tighten `description`; set `disable-model-invocation: true` |
| Skill never triggers | Add trigger terms to `description`; check `paths` scope |

Bump `metadata.version` on every structural change.

---

## Anti-Patterns

- **Wiki skill** — 50 pages in SKILL.md; fix: progressive disclosure
- **Vague description** — "helps with code"; fix: specific triggers
- **Cognitive steps** — "analyze the codebase"; fix: verb lint
- **God skill** — one skill does everything; fix: §4 decomposition
- **Orphan IR** — runtime SKILL.md drifts from design; fix: compile from IR
- **Metric fantasy** — thresholds without measurement; fix: L0/L1 first
- **Windows paths** — backslashes in path examples; fix: forward slashes
- **Vendor lock-in** — hard-coded one IDE's paths/tools; fix: portable IDs + host-adapters

---

## Additional Resources

| File | Load when |
|------|-----------|
| [QUICKSTART.md](../QUICKSTART.md) | 5-minute developer onboarding |
| [docs/index.html](../docs/index.html) | Documentation site |
| [what-is-agent-skill.md](references/what-is-agent-skill.md) | Explaining Agent Skills to authors |
| [protocol-v2.md](references/protocol-v2.md) | IR quick reference + checklist |
| [template.skill.md](references/template.skill.md) | Starting a new skill IR |
| [host-adapters.md](references/host-adapters.md) | Mapping portable tools to a specific host |
| [gap-analysis.md](references/gap-analysis.md) | Design rationale |
| [example-compiled.md](references/example-compiled.md) | Worked example: IR → SKILL.md |

---

## Quick Command

```bash
python skill-core/skill.py init my-new-skill
python skill-core/skill.py compile my-new-skill
python skill-core/skill.py test my-new-skill
python skill-core/skill.py install my-new-skill --host cursor --scope global
python skill-core/skill.py registry build && python skill-core/skill.py list
python skill-core/skill.py docs
```

Full docs: [QUICKSTART.md](../QUICKSTART.md) · [docs/index.html](../docs/index.html)
