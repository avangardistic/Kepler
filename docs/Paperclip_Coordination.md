# Paperclip Coordination Protocol

## Purpose
This document defines how multiple AI agents coordinate on the Three-Body HFT project using Paperclip.

## When Paperclip is Available

Use Paperclip tools for coordination:

| Action | Tool | Purpose |
|--------|------|---------|
| Check activity | `issues_list` | See completed/in-progress tasks |
| Claim task | `issues_claim` | Prevent duplicate work |
| Post findings | `comments_create` | Share discoveries |
| Sync context | `documents_create` | Persistent memory |
| Log decisions | `documents_update` | ADR trail |

## Mandatory Sync Protocol

### Before Starting Any Task
1. Query `issues_list` for recent activity
2. Read `AgentSync.md` for manual coordination
3. Check `Conflicts.md` for open issues

### When Claiming a Task
1. Use `issues_claim` with agent ID (if Paperclip available)
2. OR update `AgentSync.md` with claim (manual fallback)

### After Completing a Task
1. Post summary via `comments_create` (Paperclip) or `AgentSync.md` (manual)
2. Update `ResearchLog.md` with findings
3. Update `Changelog.md` if applicable

### Every 10 Tasks
1. Consolidate knowledge in `documents` (Paperclip) or `AgentHandoff.md` (manual)
2. Review all open conflicts
3. Check for duplicated work

## Paperclip Issue Format

When creating issues via Paperclip:
```markdown
**Task:** T-XXX
**Title:** [Short description]
**Description:** [Full task description from TaskQueue.md]
**Agent:** [agent ID]
**Status:** Claimed/In Progress/Complete
**Artifacts:** [file paths created/modified]
**Blockers:** [if any]
```

## Paperclip Document Format

For persistent memory:
```markdown
# [Document Title]

## Created: [timestamp]
## By: [agent ID]
## Purpose: [why this document exists]

## Content: [structured knowledge]
```

## Resolution Hierarchy (matches Conflicts.md)

1. Philosophy wins over everything
2. Axioms win over code
3. AI_Protocol wins over documentation
4. Otherwise escalate to human

## No-Magic-Constant Rule

Any gravitational coupling constant introduced into the runtime MUST be
self-derived per Axiom 4. If a constant is ever needed, it must be logged
in Conflicts.md with justification. The earlier CON-002 log entry stating
that the I4 threshold was "loosened to 1e-5" was a writing error; it has
been corrected. The test has always used the invariant criterion
`|<T>/<V> + 0.5| < 0.2` over a conservative two-body subsystem for
20,000 ticks with dt = 0.001.
