# Host Adapters

Skill-Core IR uses **portable tool IDs**. This file maps them to concrete host capabilities. Keep host-specific details here — not in the core protocol.

## Install paths

| Host | Project scope | Personal scope |
|------|---------------|----------------|
| Agent Skills (generic) | `.agents/skills/<name>/` | varies by host |
| Cursor | `.cursor/skills/<name>/` | `~/.cursor/skills/<name>/` |
| Claude Code | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` |

Copy the compiled skill folder (with `SKILL.md`) to the target path. Do not modify vendor built-in directories.

## Tool ID → host mapping

### Cursor

| Portable ID | Host capability |
|-------------|-----------------|
| `web_search` | WebSearch |
| `web_fetch` | WebFetch |
| `code_exec` | Shell |
| `file_read` | Read |
| `file_write` | Write, StrReplace |
| `search_code` | Grep, SemanticSearch, Glob |
| `sub_skill_call` | Load `SKILL.md`; user may invoke `/skill-name` |
| `subagent` | Task (subagent_type) |
| `memory_read` | Read `references/`, project rules |
| `memory_write` | Write to `references/learning.md` (with author consent) |
| `ask_user` | AskQuestion or chat prompt |

Optional frontmatter: `paths` (glob scope), `disable-model-invocation`.

### Claude Code

| Portable ID | Host capability |
|-------------|-----------------|
| `web_search` | Web search tool (if enabled) |
| `web_fetch` | Fetch URL |
| `code_exec` | Bash |
| `file_read` | Read |
| `file_write` | Write, Edit |
| `search_code` | Grep, Glob |
| `sub_skill_call` | Skill tool / slash command |
| `subagent` | Agent delegation (if available) |
| `ask_user` | AskUserQuestion |

Exact tool names may vary by Claude Code version. Prefer portable IDs in IR; adapt at compile time if needed.

### Generic / custom agent

When the host is unknown, keep IR in portable IDs and document in `compatibility`:

```yaml
compatibility: Requires bash, git, and network for documentation lookup.
```

The executing agent maps portable IDs to whatever tools it exposes.

## Frontmatter differences

All hosts support (per agentskills.io):

- `name`, `description` (required)
- `license`, `compatibility`, `metadata`, `allowed-tools` (optional)

Host-specific optional fields (use only when targeting that host):

- Cursor: `paths`, `disable-model-invocation`
- Others: check host docs before relying on extensions

## Compiling for a target host

1. Write IR with portable tool IDs (§7).
2. Pick target host(s) in Phase 0.
3. At compile time, expand Tools section using the table above if helpful.
4. Set `compatibility` to real requirements (git, python, network).
5. Omit host-only frontmatter when publishing a portable skill.
