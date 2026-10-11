# Optional External Coordination

This repository does not require Paperclip or any other external task service. Use an integration only when it is connected, available to the current contributor, and authorized for this task. Never invent an agent, issue ID, claim, or comment.

## If a shared tracker is available

- Check for overlapping work before making a claim.
- Link the repository task/conflict ID in the tracker.
- After work, report the changed files, evidence, and unresolved blockers.
- Keep the repo documents as the durable technical record; tracker comments are not a replacement for an ADR or research result.

## If it is unavailable

Use [`AgentSync.md`](AgentSync.md) for a short-lived manual claim only when multiple contributors actually share this checkout or repository state. Otherwise leave it alone. Use [`AgentHandoff.md`](AgentHandoff.md) to transfer work.

## Coordination record

A task claim prevents duplicate work; it does not settle a scientific question. The scope and evidence rules in [`AI_Protocol.md`](AI_Protocol.md) and [`../03_research/Conflicts.md`](../03_research/Conflicts.md) still apply.
