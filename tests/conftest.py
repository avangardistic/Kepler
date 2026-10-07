# conftest.py — global test-harness configuration for Kepler

"""
Why float64 is enabled here
--------------------------
JAX defaults to float32, whose machine epsilon (~1.2e-7) makes the
invariant thresholds in `docs/07_hypotheses/Invariants.md` physically
unreachable — e.g. I2 requires relative energy drift < 1e-9, and
`docs/03_physics/Symplectic.md` / Physics.md promise conservation "to
machine precision," which is a float64 concept.  Measured pre-fix drift
in float32 was 8.0e-8 on a *frozen* state (exactly float32 rounding
noise, not integrator error).

This is a precision setting, NOT a threshold loosening: all thresholds
stay exactly as defined in Invariants.md (QA_Protocol P3).  See
docs/06_research/physics/virial_theorem.md §"Energy test" and
docs/STATE_INVENTORY.md.
"""

from __future__ import annotations

import jax

jax.config.update("jax_enable_x64", True)
