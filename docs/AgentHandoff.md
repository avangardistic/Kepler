# Agent Handoff Protocol

## Purpose
Standardized protocol for transferring work between AI agents.

## Before You Stop

### 1. Update AgentSync.md
- Mark current task as completed or in-progress
- List any blockers
- Note time spent

### 2. Commit All Code
- All code changes committed with clear message
- Tests passing
- No looming conflicts

### 3. Update ResearchLog.md
- Document findings, decisions, and next steps
- Include timestamps

### 4. Update Conflicts.md
- Any open issues clearly documented
- Severity and proposed resolution noted

### 5. Post to Paperclip (if available)
- Summary comment on relevant issue
- Or create document with consolidated knowledge

## When You Start

### 1. Read AgentSync.md Completely
- Know who else is active
- See what tasks are claimed
- Check for recent discoveries

### 2. Check Conflicts.md
- Review all open conflicts
- Understand severity and proposed resolutions
- Verify CON-002 is resolved (log correction; test always used I4 criterion |<T>/<V> + 0.5| < 0.2; no threshold loosening occurred)
- Don't start work that requires conflict resolution without addressing it

### 3. Read Last 5 ResearchLog Entries
- Catch up on recent work
- Understand decisions made
- Know what's left to do

### 4. Pick a Task from TaskQueue.md
- Choose highest priority unclaimed task
- Claim it in AgentSync.md
- Start working

## Handoff Message Format

When handing off (via Paperclip comment or AgentSync update):

```markdown
## Handoff: [Agent A] → [Agent B]
**Time:** [timestamp]
**Completed:** [list]
**In Progress:** [list]
**Blocked:** [list with reasons]
**Next Priority:** [task ID]
**Notes:** [any context the next agent needs]
```

## Emergency Handoff
If you must stop immediately:
1. Save current work (commit if possible)
2. Update AgentSync.md with "EMERGENCY HANDOFF"
3. List exact file positions and next line to execute
4. Do NOT leave conflicts unresolved
