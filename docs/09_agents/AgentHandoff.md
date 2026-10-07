# Agent Handoff

> Newest session packet on top; the generic protocol follows below.

---

## Session Packet — 2026-10-07 (Session 2)
**From:** agent-arena (Arena Agent Mode, branch `arena/99b3b317-kepler`)
**To:** next agent / ANY
**Read:** `docs/00_INDEX.md` → `docs/STATE_INVENTORY.md` → this packet. That's the whole 5 minutes.

### 1. What Was Done This Session
- Full state audit (measured, not assumed) — the incoming brief's claims were
  wrong in 3 places; all logged in `docs/ResearchLog.md` + `STATE_INVENTORY.md`.
- Reorganized 47 flat docs into the 12 numbered categories + `00_INDEX.md` +
  `06_research/` registry (git mv history preserved; `generate_docs.py`
  retargeted so regeneration reproduces the tree).
- Resolved R-PHY-001 (virial): the "T/V → −1.0" was a **double artifact** —
  unphysical 1-D radial-plunge ICs (F10: numerical heating −0.115 → +296)
  AND a test assignment bug (`V` actually held integrate()'s ratio output;
  reported ratio was the identity Ē/V̄ − 1 ≈ −1.0008). Circular orbits do not
  exist in 1-D; the brief's recommended "v_circ fix in 1-D" also fails.
- Fixed `src/physics_jax.py`: isotropic multi-D softening, shape-safe
  `acceleration`, consistent imbalance statistic; added `src/__init__.py`.
- Rebuilt `test_virial_ratio_convergence` on a 2-D circular orbit
  (v = √(G·m·r)/d = 0.25; T/V = −0.5 exactly). Thresholds UNTOUCHED (0.2).
- Added `tests/conftest.py` enabling float64 — the only way to meet I2's
  pre-existing 1e−9 threshold in float32-era JAX; precision, not loosening.
- Fixed the previously *unreported* I2 failure (same float64 root cause).
- Opened **CON-003** (G fallback `1.0` + frozen-vs-running G spec divergence) —
  needs a human/ADR decision; do not silently patch the engine.

### 2. Current Test Status (verified this session)
9 total · **9 passing** · 0 failing · 0 skipped (`python -m pytest tests/ -v`).

### 3. Next Session MUST Do
1. `python -m pytest tests/ -v` — trust measurement over any brief.
2. Pick from `06_research/README.md`: **R-PHY-002** (G_eff decision, HIGH —
   gates honest wording of H2/I2) or R-PHY-003 T-009 (preflight helper + dt
   sweep) or T-008 (generalized-virial test for R-PHY-004).
3. If the human passes a decision on CON-003, implement + record in
   `11_meta/Decisions.md`, then update Physics.md.
4. Apply Five Whys if stuck; FMEA before implementation; update AgentSync +
   ResearchLog + STATE_INVENTORY at session end. ALWAYS.

### 4. Critical Constraints (Never Violate)
No filters / indicators / risk-management / external parameters · time = tick ·
never loosen test thresholds (0.2 for I4, 1e−9 for I2 — both proven
attainable now) · Philosophy/Axioms/AI_Protocol are human-only · every failure
gets a FailureModes entry, every decision a Decisions entry.

### 5. Known Blockers
- CON-003 (decision required; engine behavior pinned meanwhile).
- No `pyproject.toml` / CI; environment must be bootstrapped manually:
  `pip install "jax[cpu]" pytest` (float64 comes from `tests/conftest.py`).
- JAX ≥ 0.4 assumed (tested on 0.10.2 / CPU).

### 6. Files Changed This Session
`docs/**` (reorg + new: `00_INDEX.md`, `STATE_INVENTORY.md`, `06_research/**`,
updated FailureModes F10/F8, Conflicts CON-002→RESOLVED/CON-003, Hypotheses H2,
Invariants I2/I4 notes, Physics.md notes, ResearchLog, AgentSync, this packet,
Changelog v0.6.0, TaskQueue T-003/T-004 closed + T-008/T-009 added),
`src/physics_jax.py`, `src/__init__.py` (new), `tests/conftest.py` (new),
`tests/test_physics.py`, `generate_docs.py`.

### 7. Recommended First Actions
```bash
python -m pytest tests/ -v
cat docs/00_INDEX.md
cat docs/06_research/README.md
# then open 06_research/physics/gravity_derivation.md (R-PHY-002)
```

---

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
