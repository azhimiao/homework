# Worked Example: IR → Compiled SKILL.md

This shows how Skill Protocol v2 IR compiles to a runtime skill. Example: `format-commit-message`.

---

## IR Excerpt (abbreviated)

### §1 Intent
- **Goal:** Generate conventional commit messages from staged git diff.
- **Context:** User asks for commit message, or before `git commit`.
- **Constraints:** Time < 30s; no push; read-only git except message output.

### §4 Decomposition
- **S1:** read-staged-diff — inputs: repo_path → outputs: diff_text
- **S2:** classify-change — inputs: diff_text → outputs: type, scope, breaking
- **S3:** compose-message — inputs: type, scope, summary → outputs: message

### §5 Execution Plan
1. RUN `git status` and `git diff --staged`
2. PARSE diff into file list and change summary
3. CLASSIFY change type (feat|fix|docs|…) from diff patterns
4. GENERATE message per conventional commits template
5. VALIDATE message length ≤ 72 chars subject line

### §3 Output Profile: `narrative`

---

## Compiled SKILL.md

```markdown
---
name: format-commit-message
description: >-
  Generates conventional commit messages by analyzing staged git diffs. Use when
  the user asks for a commit message, help writing a commit, or before running
  git commit. Triggers on "commit message", "conventional commit", "what should I
  commit", or staged changes review.
metadata:
  version: "1.0.0"
  status: stable
  protocol: skill-core-v2
compatibility: Requires git repository
---

# Format Commit Message

## Quick Start

1. Run `git status` and `git diff --staged`
2. Classify change type from diff (feat, fix, docs, refactor, test, chore)
3. Draft subject line ≤ 72 chars; optional body with bullet points
4. Present message in a fenced code block for copy-paste

## Workflow

### Step 1: Gather staged changes
```bash
git status
git diff --staged
```
IF no staged changes → ASK user to stage files first; STOP.

### Step 2: Classify
IF new feature → type `feat`
IF bug fix → type `fix`
IF docs only → type `docs`
IF test only → type `test`
ELSE → type `chore` or `refactor` based on diff

Scope = primary directory or module touched (optional).

### Step 3: Compose
Format:
```
<type>(<scope>): <subject>

<body — what and why, not how>
```

### Step 4: Validate
- Subject ≤ 72 characters
- Imperative mood ("add" not "added")
- Body explains why if non-obvious

## Outputs

Narrative profile — present as:
- `# Suggested commit message` with fenced block
- `# Rationale` — one paragraph on type/scope choice

## Tools

| Tool | Use |
|------|-----|
| Shell | git status, git diff --staged |

## Failure Modes

| ID | Signal | Recovery |
|----|--------|----------|
| F1 | No staged changes | Ask user to `git add` |
| F2 | Not a git repo | Report; suggest `git init` |
| F3 | Diff too large (>500 lines) | Summarize by directory; ask user for focus |

## Verification (L1)

| Test | Input | Expected |
|------|-------|----------|
| T1 | Single file feat diff | `feat(scope): ...` |
| T2 | Empty staged | Ask to stage |
| T3 | Docs-only diff | `docs: ...` |
```

---

## What Changed in Compilation

| IR | Runtime |
|----|---------|
| §1 Goal + Context | YAML `description` |
| §1 Constraints | `compatibility` |
| §4 S1–S3 | Condensed into Workflow (not separate skills — small enough) |
| §5 5 steps | Quick Start + Workflow |
| §6 Decision IFs | Inline in Workflow |
| §3 narrative profile | Outputs section |
| §7 Shell only | Tools table |
| §10 F1–F3 | Failure Modes table |
| §9 L1 tests | Verification section |
| §12 depends_on: skill-core | Implicit; not in runtime body |
| §13 version | metadata.version |

**Note:** S1–S3 stayed inline because the skill is small. IR §4 rule: if |S| > 5 or sub-skills are reused elsewhere, extract to separate skill folders.
