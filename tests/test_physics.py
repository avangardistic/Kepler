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
I2  Total energy conserved           (relative drift < 1e-9 per step)
I4  Virial ratio → −½                (|T/V + ½| < 0.2 over long run)
I6  |Imbalance| ≤ 1                  (always)
I7  Spread > 0  ⇒  bid < ask        (always; checked in state construction)

Hypotheses
-----------
H1  ‖L‖ bounded                      (same as I1)
H2  T/V → −1/2                       (same as I4)
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
    compute_kinetic_energy,
    compute_potential_energy,
    compute_total_energy,
    compute_virial_ratio,
    compute_imbalance,
    symplectic_step,
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
# I4 / H2 — virial ratio → −½
# ------------------------------------------------------------------

def test_virial_ratio_convergence() -> None:
    """H2 / I4: generalized virial theorem for conservative subsystem.

    Tests the generalized virial theorem for a CONSERVATIVE subsystem
    (no friction, no external forces):

        2<T> + <V> = 0  ->  <T>/<V> = -0.5

    For systems WITH friction and external forces, see
    Physics.md §Virial Theorem (Generalized).

    Criterion: |<T>/<V> + 0.5| < 0.2 (from Invariants.md I4).
    """
    # Two-body system with initial velocities tuned for approximate
    # virial equilibrium (circular orbit velocity)
    # Use self-induced gravity (None = compute from state per Axiom 4)
    
    # Two equal masses, separation d=2, in near-circular orbit
    x = jnp.array([-1.0, 1.0])
    m = jnp.array([1.0, 1.0])
    # Small velocity perturbation — system will oscillate around equilibrium
    v = jnp.array([0.1, -0.1])
    I = jnp.zeros(2)       # No external force
    gamma = jnp.zeros(2)   # No friction (conservative subsystem)
    state = ThreeBodyState(x=x, v=v, m=m, I=I, gamma=gamma)

    n = 20_000
    dt = 0.001  # Small dt for good conservation
    L, E, V, _ = integrate(state, n, G=None, dt=dt)

    # Compute T = E - V at each tick
    T = E - V

    # Skip equilibration period (first 5000 ticks)
    skip = 5_000
    T_post = T[skip:]
    V_post = V[skip:]

    # Time-averaged virial ratio
    T_avg = jnp.mean(T_post)
    V_avg = jnp.mean(V_post)
    ratio_avg = T_avg / V_avg if abs(V_avg) > 1e-10 else 0

    print(f"After {skip} ticks: <T>={T_avg:.6f}, <V>={V_avg:.6f}")
    print(f"  <T>/<V> = {ratio_avg:.6f} (target: -0.5)")
    print(f"  |<T>/<V> + 0.5| = {abs(ratio_avg + 0.5):.6f}")

    # Criterion from Invariants.md: |<T>/<V> + 0.5| < 0.2 for I4
    deviation = abs(ratio_avg + 0.5)
    
    assert deviation < 0.2, (
        f"H2/I4 rejected: virial ratio deviation {deviation:.4f} > 0.2 "
        f"(<T>={T_avg:.4f}, <V>={V_avg:.4f}, ratio={ratio_avg:.4f})"
    )

    # Check angular momentum bounded (H1)
    L_max = jnp.max(L)
    L_mean = jnp.mean(L)
    print(f"Angular momentum: mean={L_mean:.6f}, max={L_max:.6f}")
    # For this 1D system with no angular motion, L should stay ~0
    assert L_max < 1.0, f"H1 failed: L grew to {L_max}"

    # Check virial ratio is finite (not the main test, just sanity)
    virial = T / jnp.where(jnp.abs(V) > 1e-10, V, 1e-10)
    virial_finite = jnp.all(jnp.isfinite(virial))
    print(f"Virial ratio finite: {virial_finite}")
    assert virial_finite, "Virial ratio went non-finite"


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
