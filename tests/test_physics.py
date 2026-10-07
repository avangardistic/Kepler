# test_physics.py — Invariant and hypothesis tests for physics_jax

"""
Validates the core invariants and hypotheses from Invariants.md and
Hypotheses.md on the ThreeBodyState produced by physics_jax.py.

Every test is deterministic and self-contained — no network, no disk,
no external data.  Synthetic L2 books are constructed in code to exercise
each invariant boundary.

Invariants
----------
I1  Angular momentum bounded          (H1: ‖L‖ ≤ 10·L̄ in 95% of ticks)
I2  Total energy conserved           (relative drift < 1e-9; requires
                                      float64 — see tests/conftest.py)
I4  Virial ratio → −½                (|T/V + ½| < 0.2; tested on the only
                                      conservative configuration where −½ is
                                      instantaneously exact: a 2-D circular
                                      orbit.  See R-PHY-001 / FailureModes F10
                                      for why 1-D bound orbits cannot work.)
I6  |Imbalance| ≤ 1                  (always)
I7  Spread > 0  ⇒  bid < ask        (always; checked in state construction)

Hypotheses
-----------
H1  ‖L‖ bounded                      (same as I1)
H2  T/V → −1/2                       (same as I4; REVISED claim wording in
                                      docs/07_hypotheses/Hypotheses.md)
H3  Π ∝ ∫|L| dt  (proxy: recorded here, tested on simulation data)
H7  Hedge constraint |φ| < 1e-6     (tested in test_mm.py)
"""

from __future__ import annotations

import jax
import jax.numpy as jnp
import pytest

from src.physics_jax import (
    ThreeBodyState,
    compute_angular_momentum,
    integrate,
    state_from_l2,
)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def make_book(prices: list[float], quantities: list[float]) -> jnp.ndarray:
    """Build a (K, 2) L2 book array (price, quantity)."""
    return jnp.array(list(zip(prices, quantities)))


def balanced_book(mid: float = 100.0,
                  spread: float = 0.1,
                  depth: float = 10.0) -> tuple[jnp.ndarray, jnp.ndarray]:
    """Symmetric balanced L2: bids descending, asks ascending."""
    asks = make_book([mid + spread / 2 + i * 0.05 for i in range(5)],
                     [depth] * 5)
    bids = make_book([mid - spread / 2 - i * 0.05 for i in range(5)][::-1],
                     [depth] * 5)
    return bids, asks


@pytest.fixture
def symmetric_state() -> ThreeBodyState:
    """Three identical balanced bodies ⇒ L=0, E<0, virial≈−½ (at rest)."""
    b, a = balanced_book(mid=100.0, spread=0.1, depth=10.0)
    return state_from_l2(b, a, b, a, b, a)


# ------------------------------------------------------------------
# I1 / H1 — angular momentum bounded
# ------------------------------------------------------------------

def test_angular_momentum_zero_at_rest(symmetric_state: ThreeBodyState) -> None:
    """At rest with symmetric positions, L = 0 exactly."""
    L = compute_angular_momentum(symmetric_state)
    assert jnp.allclose(L, 0.0), f"Expected L=0, got {L}"


def test_angular_momentum_bounded_over_10k_ticks(symmetric_state: ThreeBodyState) -> None:
    """H1: ‖L‖ must stay below 10·L̄ over 10 000 ticks (≥95% of time).

    Because the configuration is symmetric, the true L̄ should be tiny;
    any blow-up indicates a bug in the integrator.
    """
    n_ticks = 10_000
    # Use self-induced gravity (None = compute from state)
    L_norm, *_ = integrate(symmetric_state, n_ticks, G=None)
    L_bar = jnp.mean(L_norm)
    threshold = 10.0 * jnp.maximum(L_bar, 1e-12)
    violations = jnp.sum(L_norm > threshold) / n_ticks
    # At most 5% of ticks may exceed 10·L̄
    assert violations < 0.05, (
        f"H1 rejected: {violations:.2%} of ticks exceed 10·L̄"
    )


# ------------------------------------------------------------------
# I2 — energy conservation (relative drift < 1e-9 per step)
# ------------------------------------------------------------------

def test_energy_conservation_relative_drift(symmetric_state: ThreeBodyState) -> None:
    """I2: |E_t − E_0| / |E_0| < 1e-9 for a few hundred ticks."""
    n = 200
    # Use self-induced gravity (None = compute from state)
    _, energy, *_ = integrate(symmetric_state, n, G=None)
    E0 = energy[0]
    rel_drift = jnp.max(jnp.abs(energy - E0) / jnp.maximum(jnp.abs(E0), 1e-12))
    assert rel_drift < 1e-9, (
        f"I2 rejected: max relative energy drift {rel_drift:.2e}"
    )


# ------------------------------------------------------------------
# I4 / H2 — virial ratio → −½  (2-D circular orbit)
# ------------------------------------------------------------------

def test_virial_ratio_convergence() -> None:
    """H2 / I4: virial ratio of a conservative circular orbit is −½.

    History of this test (see docs/06_research/physics/virial_theorem.md):
    it previously used 1-D initial conditions (x=∓1, v=±0.1) and reported
    ⟨T⟩/⟨V⟩ → −1.0008.  Two compounding defects:
    (1) Unphysical setup — in 1-D every bound orbit is a RADIAL PLUNGE (zero
        angular momentum ⇒ no centrifugal barrier); close approaches are
        unresolved at dt=1e-3, numerical heating drives E −0.115 → +296 and
        the pair escapes.  Setting v = v_circ in 1-D fails identically
        (E −0.0625 → +160): a circular orbit does not exist in 1-D.
    (2) Test bug — `L, E, V, _ = integrate(...)` bound the 3rd return value
        (the per-tick VIRIAL RATIO T/V) to a variable named `V`, so the old
        "<V>" was really ⟨T/V⟩ (dominated by the |V|<ε division guard once the
        pair escaped, mean −376,445) and "<T>" was fabricated as E − T/V.
        The reported −1.0008 = Ē/V̄ − 1 was an algebraic echo measuring nothing.

    Correct conservative setup: a genuine circular orbit needs an
    angular-momentum barrier, i.e. >= 2-D motion.  Two equal masses m = 1,
    half-separation r = d/2 = 1, self-induced G = 1/⟨d²⟩ = 1/4 (Axiom 4,
    computed from the initial state exactly as integrate() does):

        per-body centripetal balance:  m v² / r = G m² / d²
        ⇒  v_circ = sqrt(G·m·r / d²) = sqrt(0.25·1·1 / 4) = 0.25
           (equivalently v_rel = sqrt(G(m₁+m₂)/d) = 0.5, split equally)

        T = ½·2·m·v² = 0.0625 ,   V = −G·m²/d = −0.125
        ⇒  T/V = −1/2  EXACTLY, and constant at every tick.

    Criterion: |T/V + 0.5| < 0.2 (from Invariants.md I4) — UNCHANGED.
    For a circular orbit it is checked both instantaneously (max over
    ticks) and on the time-average; friction and external imbalance are
    zero so the generalized theorem (Physics.md §Virial Generalized)
    reduces to the standard form.  The 1-D radial-infall configuration is
    kept as a documented failure mode (F10), not as a passing test.
    """
    x = jnp.array([[-1.0, 0.0], [1.0, 0.0]])
    # Tangential velocities ⇒ exact circular orbit (derivation above)
    v = jnp.array([[0.0, -0.25], [0.0, 0.25]])
    m = jnp.array([1.0, 1.0])
    I = jnp.zeros(2)       # No external force  (conservative subsystem)
    gamma = jnp.zeros(2)   # No friction        (conservative subsystem)
    state = ThreeBodyState(x=x, v=v, m=m, I=I, gamma=gamma)

    n = 20_000
    dt = 0.001
    # integrate() freezes G = compute_self_induced_G(state_0) = 1/⟨d²⟩ = 0.25,
    # consistent with the v_circ derivation above.
    L_norm, energy, virial, _ = integrate(state, n, G=None, dt=dt)

    skip = 5_000
    vir_post = virial[skip:]
    dev_mean = float(abs(jnp.mean(vir_post) + 0.5))
    dev_max = float(jnp.max(jnp.abs(vir_post + 0.5)))
    print(f"virial: mean={float(jnp.mean(vir_post)):.6f}, "
          f"|dev_mean|={dev_mean:.2e}, |dev_max|={dev_max:.2e}")

    # Invariants.md I4 criterion, unchanged: deviation < 0.2
    assert dev_mean < 0.2, f"H2/I4 rejected: mean dev {dev_mean:.4f} > 0.2"
    # Circular orbit ⇒ the stronger per-tick statement must also hold.
    assert dev_max < 0.2, f"H2/I4 rejected: per-tick dev {dev_max:.4f} > 0.2"

    # Side-checks on the same trajectory:
    # I2 — energy conserved along the circular orbit (float64, see conftest)
    E0 = energy[0]
    rel_drift = jnp.max(jnp.abs(energy - E0) / jnp.abs(E0))
    print(f"energy: E0={float(E0):.6f}, max rel drift={float(rel_drift):.2e}")
    assert rel_drift < 1e-9, f"I2 rejected on circular orbit: {rel_drift:.2e}"

    # H1 — angular momentum bounded (here L ≈ 0.5, m r v ×2 bodies)
    L_max, L_mean = float(jnp.max(L_norm)), float(jnp.mean(L_norm))
    print(f"angular momentum: mean={L_mean:.6f}, max={L_max:.6f}")
    assert L_max < 1.0, f"H1 failed: L grew to {L_max}"

    # Sanity: everything finite
    assert jnp.all(jnp.isfinite(virial)), "Virial ratio went non-finite"


# ------------------------------------------------------------------
# I6 — |Imbalance| ≤ 1
# ------------------------------------------------------------------

def test_imbalance_always_bounded(symmetric_state: ThreeBodyState) -> None:
    """I6: every body's |I_i| ≤ 1 at every tick."""
    _, _, _, imb = integrate(symmetric_state, 5_000, G=None)
    assert jnp.all(imb <= 1.0 + 1e-12), (
        f"I6 rejected: |I| exceeded 1, max {jnp.max(imb)}"
    )


# ------------------------------------------------------------------
# Edge cases
# ------------------------------------------------------------------

def test_jump_to_zero_depth_freezes_state() -> None:
    """F1: zero depth ⇒ mass→0, L→0, no explosion.

    Construct a body with empty book and confirm the integrator doesn't
    produce NaN or Inf.
    """
    empty_book = make_book([], [])
    b, a = balanced_book()
    state = state_from_l2(b, a, empty_book, empty_book, b, a)
    # State should have finite values even for the empty book body
    assert jnp.all(jnp.isfinite(state.x)), "State x not finite"
    assert jnp.all(jnp.isfinite(state.m)), "State m not finite"
    assert jnp.all(jnp.isfinite(state.I)), "State I not finite"
    # Now integrate (use self-induced G)
    L_norm, energy, virial, imb = integrate(state, 100, G=None)
    assert jnp.all(jnp.isfinite(L_norm)), "F1: L went non-finite after zero-depth"
    assert jnp.all(jnp.isfinite(energy)), "F1: energy went non-finite"
    assert jnp.all(jnp.isfinite(virial)), "F1: virial went non-finite"
    assert jnp.all(jnp.isfinite(imb)), "F1: imbalance went non-finite"


def test_epsilon_softening_prevents_overflow() -> None:
    """F4: two bodies at essentially the same microprice must not explode."""
    b1, a1 = balanced_book(mid=100.0, spread=0.1, depth=10.0)
    b2, a2 = balanced_book(mid=100.0 + 1e-12, spread=0.1, depth=10.0)  # almost same
    state = state_from_l2(b1, a1, b2, a2, b1, a1)
    L_norm, *_ = integrate(state, 50, G=None)
    assert jnp.all(jnp.isfinite(L_norm)), "F4: 1/d³ blowup with near-collision"


# ------------------------------------------------------------------
# H3 proxy — record Π-structure (Π = ∮p·dx, approximated by cumulative L-area)
# ------------------------------------------------------------------

def test_cumulative_angular_momentum_recorded(symmetric_state: ThreeBodyState) -> None:
    """H3 groundwork: L(t) is finite and non-divergent over 100k ticks.

    Π ∝ ∫ ‖L‖ dt is computed in simulation_live_v3; here we confirm
    L stays finite so the integral is well-defined.
    """
    n = 100_000
    L_norm, *_ = integrate(symmetric_state, n, G=None)
    assert jnp.all(jnp.isfinite(L_norm)), "H3: L diverged → Π undefined"
    # Sanity: mean |L| should be non-zero for non-symmetric cases;
    # for this symmetric case it must be ~0.
    assert jnp.mean(L_norm) < 1e-3, "H3: unexpected L in symmetric rest state"


# ------------------------------------------------------------------
# Determinism (no randomness anywhere in physics)
# ------------------------------------------------------------------

def test_integrate_deterministic(symmetric_state: ThreeBodyState) -> None:
    """Same initial state + same n_ticks ⇒ identical trajectory."""
    _, a, _, _ = integrate(symmetric_state, 1_000, G=None)
    _, b, _, _ = integrate(symmetric_state, 1_000, G=None)
    assert jnp.allclose(a, b, atol=1e-15), "Physics must be fully deterministic"
