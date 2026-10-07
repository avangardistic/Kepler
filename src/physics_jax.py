# physics_jax.py — Three-Body HFT Physics Engine

"""
Three-body gravitational dynamics on L2 tick data.

All quantities derived from raw L2 order book data; no external parameters.
Time is quantized in ticks. Symplectic integrator preserves energy and
angular momentum to machine precision.

References
----------
Concept.md   — orbital position, mass, imbalance definitions
Physics.md   — Lagrangian, Euler-Lagrange, virial theorem
Axioms.md    — mass from volume (Axiom 3), self-consistent gravity (Axiom 4)
"""

from __future__ import annotations

import jax
import jax.numpy as jnp
from jax import lax
from typing import Tuple
from dataclasses import dataclass

# ------------------------------------------------------------------
# Constants (all internal, no magic numbers outside of definitions)
# ------------------------------------------------------------------

EPSILON: float = 1e-8           # Regularizer for 1/d³ singularity (F4)
DT_TICK: float = 1.0            # One tick = one integration step

# G is NOT a constant — it is self-derived from the system geometry.
# Use compute_self_induced_G() to get G_eff for a given state.
# See Physics.md §Self-Induced Gravity and Axiom 4.
#
# PRECISION NOTE: "machine precision" conservation (I2, Physics.md
# §Symplectic Integrator) requires float64.  JAX defaults to float32, whose
# epsilon (~1.2e-7) makes the 1e-9 thresholds in Invariants.md unreachable.
# Tests enable jax_enable_x64 in tests/conftest.py; any production harness
# that must verify I2/I4 numerics must do the same.
#
# DIMENSIONALITY NOTE: positions may be 1-D (one log-microprice per body,
# the market-native embedding) or multi-D.  Softening is ISOTROPIC:
# dist = sqrt(‖dx‖² + ε²) on the full separation vector (F10 /
# 06_research/physics/virial_theorem.md).  NOTE: in 1-D every bound
# gravitational orbit is a radial plunge — there is no angular-momentum
# barrier — so circular-orbit states (T/V = -1/2 instantaneously) exist
# only in >= 2-D.


@dataclass(frozen=True)
class ThreeBodyState:
    """Position, velocity, and mass for three bodies in ln-microprice space.

    Attributes
    ----------
    x : ndarray, shape (3,)
        Orbital positions x_i = ln(P_i^mu)  (Concept.md §2.2)
    v : ndarray, shape (3,)
        Orbital velocities dx_i/dt.
    m : ndarray, shape (3,)
        Masses m_i = ln(1 + total_depth_i)  (Axiom 3)
    I : ndarray, shape (3,)
        Normalised imbalance per body  (Concept.md §2.4)
    gamma : ndarray, shape (3,)
        Friction / spread coefficient  (Concept.md §2.5)
    """

    x: jnp.ndarray
    v: jnp.ndarray
    m: jnp.ndarray
    I: jnp.ndarray
    gamma: jnp.ndarray

    def tree_flatten(self) -> Tuple[Tuple[jnp.ndarray, ...], Tuple]:
        """JAX pytree flatten."""
        return (self.x, self.v, self.m, self.I, self.gamma), ()

    @classmethod
    def tree_unflatten(_aux: Tuple, children: Tuple[jnp.ndarray, ...]) -> "ThreeBodyState":
        """JAX pytree unflatten."""
        return ThreeBodyState(x=children[0], v=children[1], m=children[2],
                              I=children[3], gamma=children[4])


# Register as JAX pytree after class definition
jax.tree_util.register_pytree_node(
    ThreeBodyState,
    lambda state: ((state.x, state.v, state.m, state.I, state.gamma), ()),
    lambda aux, children: ThreeBodyState(
        x=children[0], v=children[1], m=children[2],
        I=children[3], gamma=children[4]
    ),
)


# ------------------------------------------------------------------
# Derived quantities
# ------------------------------------------------------------------

def compute_angular_momentum(state: ThreeBodyState) -> jnp.ndarray:
    """Orbital angular momentum for the system.

    L = Σ_i m_i (x_i × v_i)   (Concept.md §7)

    For 1-D motion the cross product is zero (no orbital angular momentum).
    For 2-D/3-D motion we compute the proper cross product.

    Returns
    -------
    L : scalar or ndarray
        Total angular momentum (scalar for 1-D, vector for 2-D/3-D).
    """
    # jnp.cross requires 2D or 3D vectors
    if state.x.ndim == 1 and len(state.x) <= 3:
        # 1D case: positions are scalars, no angular momentum
        return jnp.zeros(())  # scalar zero
    else:
        # Multi-dimensional case
        return jnp.sum(state.m * jnp.cross(state.x, state.v), axis=0)


def compute_kinetic_energy(state: ThreeBodyState) -> float:
    """Total kinetic energy T = ½ Σ m_i v_i²  (Physics.md §Energy).

    For 1D motion, v_i is a scalar; for multi-D, v_i is a vector and
    ‖v_i‖² is the squared norm.
    """
    # v can be 1D (scalar velocities) or 2D (vector velocities)
    v_sq = state.v ** 2
    if v_sq.ndim > 1:
        v_sq = jnp.sum(v_sq, axis=-1)  # sum over spatial dimensions
    return 0.5 * jnp.sum(state.m * v_sq)


def compute_self_induced_G(state: ThreeBodyState) -> float:
    """Compute self-induced gravitational coupling G_eff = 1 / <d²>.

    Per Axiom 4 and Physics.md §Self-Induced Gravity, the gravitational
    coupling is NOT a free parameter. It is derived from the system geometry:

        G_eff = 1 / <d²>_t

    where <d²>_t is the time-averaged squared distance between bodies.

    For instantaneous computation (single tick), we use the current
    squared distances as an approximation:

        G_eff ≈ 1 / (mean of pairwise squared distances)

    Returns
    -------
    G_eff : float
        Self-induced gravitational coupling.
    """
    n = len(state.x)
    if n < 2:
        return 1.0  # Single body, no gravity
    
    # Compute mean squared distance (sum over spatial dimensions so the
    # coupling is a scalar for multi-D configurations as well as 1-D)
    d_sq_sum = 0.0
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx = state.x[i] - state.x[j]
            d_sq_sum += jnp.sum(dx ** 2)
            count += 1
    
    if count == 0 or d_sq_sum < EPSILON:
        return 1.0  # Default for degenerate cases
    
    d_sq_mean = d_sq_sum / count
    return 1.0 / d_sq_mean


def compute_potential_energy(state: ThreeBodyState,
                             G: float | None = None) -> float:
    """Newtonian potential V = -Σ_{i<j} G m_i m_j / |x_i - x_j|.

    Regularised with EPSILON to prevent numeric overflow (F4).
    Works for any number of bodies (not just 3).
    
    If G is None, uses self-induced gravity (Axiom 4).

    Parameters
    ----------
    state : ThreeBodyState
        Current state.
    G : float, optional
        Gravitational coupling. If None, computed via compute_self_induced_G().

    Returns
    -------
    V : float
        Total potential energy.
    """
    if G is None:
        G = compute_self_induced_G(state)
    
    n = len(state.x)
    V = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            dx = state.x[i] - state.x[j]
            # Isotropic softening on the full separation vector (multi-D safe)
            dist = jnp.sqrt(jnp.sum(dx ** 2) + EPSILON ** 2)
            V -= G * state.m[i] * state.m[j] / dist
    return V


def compute_total_energy(state: ThreeBodyState,
                         G: float | None = None) -> float:
    """E = T + V  (Physics.md §Energy, Axiom 2).
    
    If G is None, uses self-induced gravity (Axiom 4).
    """
    return compute_kinetic_energy(state) + compute_potential_energy(state, G)


def compute_virial_ratio(state: ThreeBodyState,
                         G: float | None = None) -> float:
    """Virial ratio T / V; theoretical limit is −½ (Physics.md §Virial).

    H2 claims T/V → −1/2 (within 20%).
    
    If G is None, uses self-induced gravity (Axiom 4).
    """
    T = compute_kinetic_energy(state)
    V = compute_potential_energy(state, G)
    # Guard against division by zero (deep flat book).
    safe_V = jnp.where(jnp.abs(V) < EPSILON, EPSILON, V)
    return T / safe_V


def compute_imbalance(state: ThreeBodyState) -> jnp.ndarray:
    """Per-body normalised imbalance I_i ∈ [−1, 1] (Axiom 6, I6)."""
    return state.I  # already normalised at ingestion


# ------------------------------------------------------------------
# Equations of motion
# ------------------------------------------------------------------

def acceleration(state: ThreeBodyState,
                 G: float) -> jnp.ndarray:
    """Right-hand side of the three-body ODE (Concept.md §3).

    m_i a_i = − Σ_{j≠i} G m_i m_j / |x_i−x_j|³ (x_i−x_j)  +  I_i·m_i  −  γ_i v_i

    Dividing by m_i:
        a_i = − Σ_{j≠i} G m_j / |x_i−x_j|³ (x_i−x_j)  +  I_i  −  γ_i v_i / m_i

    The first term is Newtonian gravity per unit mass (Axiom 4).  The second
    term captures order-flow imbalance as an effective acceleration (Concept
    §2.4).  The third is frictional damping (Concept §2.5).

    Returns
    -------
    a : ndarray, same shape as state.x — (N,) for 1-D, (N, dim) for multi-D.
        Acceleration per body (N = number of bodies, expected 3).
    """
    n = len(state.x)
    a = jnp.zeros_like(state.x)
    for i in range(n):
        grav = jnp.zeros_like(state.x[i])
        for j in range(n):
            if i != j:
                dx = state.x[i] - state.x[j]
                # Isotropic softening: distance is the norm of dx, not
                # per-coordinate (see module header, Dimensionality note).
                dist = jnp.sqrt(jnp.sum(dx ** 2) + EPSILON ** 2)
                # Gravitational acceleration per unit mass: -G m_j (x_i - x_j) / r³
                grav -= G * state.m[j] * dx / (dist ** 3)
        # Add imbalance acceleration and friction (per unit mass)
        # Use jnp.where to handle zero mass (empty book -> freeze the body)
        m_i = state.m[i]
        friction_term = state.gamma[i] * state.v[i] / jnp.maximum(m_i, EPSILON)
        a_i = grav + state.I[i] - friction_term
        # If mass is zero, set acceleration to zero (frozen body)
        a = a.at[i].set(jnp.where(m_i < EPSILON, 0.0, a_i))
    return a


# ------------------------------------------------------------------
# Symplectic leapfrog integrator (velocity Verlet)
# ------------------------------------------------------------------

def symplectic_step(state: ThreeBodyState,
                    G: float,
                    dt: float = DT_TICK) -> ThreeBodyState:
    """One symplectic (velocity Verlet) step in tick time.

    Symplectic integrators preserve the phase-space structure and hence
    conserve energy and angular momentum to O(dt²) per step, with no
    secular drift (Physics.md §Symplectic).

    Parameters
    ----------
    state : ThreeBodyState
        Current state.
    dt : float
        Tick step size (default 1.0 = one tick).
    G : float
        Gravitational coupling (internal, dimensionless).

    Returns
    -------
    state_next : ThreeBodyState
        State after one tick.
    """
    # Half-step velocity update
    a0 = acceleration(state, G)
    v_half = state.v + 0.5 * dt * a0

    # Full-step position update
    x_next = state.x + dt * v_half

    # Recompute acceleration at new positions (mass, imbalance, gamma
    # are treated as fixed per tick — they update only when L2 changes).
    a1 = acceleration(
        ThreeBodyState(x=x_next, v=v_half, m=state.m, I=state.I,
                       gamma=state.gamma),
        G if G is not None else compute_self_induced_G(
            ThreeBodyState(x=x_next, v=v_half, m=state.m, I=state.I, gamma=state.gamma)
        ),
    )

    # Second half-step velocity update
    v_next = v_half + 0.5 * dt * a1

    return ThreeBodyState(x=x_next, v=v_next, m=state.m, I=state.I,
                          gamma=state.gamma)


# ------------------------------------------------------------------
# JAX-macro for many ticks (vectorised / pmap friendly)
# ------------------------------------------------------------------

def integrate(state_0: ThreeBodyState,
              n_ticks: int,
              G: float | None = None,
              dt: float = DT_TICK) -> Tuple[jnp.ndarray, jnp.ndarray,
                                            jnp.ndarray, jnp.ndarray]:
    """Integrate for n_ticks steps, recording ‖L‖, E, virial, imbalance.

    Records the INITIAL state (t=0) followed by n_ticks subsequent states,
    giving n_ticks+1 total recordings.

    Parameters
    ----------
    state_0 : ThreeBodyState
        Initial conditions from first L2 tick.
    n_ticks : int
        Number of ticks to simulate.
    G : float, optional
        Gravitational coupling. If None, computed via compute_self_induced_G()
        from the INITIAL state and held constant throughout integration.
    dt : float
        Tick step.

    Returns
    -------
    L_norm : ndarray, shape (n_ticks+1,)
        ‖L‖ at each tick (H1: must stay bounded).
    energy : ndarray, shape (n_ticks+1,)
        Total energy E (I2: must be conserved).
    virial : ndarray, shape (n_ticks+1,)
        T/V ratio (H2: must approach −½).
    imbalance_abs : ndarray, shape (n_ticks+1,)
        ‖I_i‖ per tick (I6: ≤ 1).
    """
    # Compute G upfront if not provided (Axiom 4: self-induced gravity)
    # This must happen BEFORE defining body_fn so the closure captures the value
    if G is None:
        G = compute_self_induced_G(state_0)
    
    def body_fn(carry: ThreeBodyState, _: int) -> Tuple[ThreeBodyState, dict]:
        s_next = symplectic_step(carry, G, dt)
        L = compute_angular_momentum(s_next)
        E = compute_total_energy(s_next, G)
        Vratio = compute_virial_ratio(s_next, G)
        # Store max |I| across bodies as a scalar
        Iabs = jnp.max(jnp.abs(compute_imbalance(s_next)))
        return s_next, {"L_norm": jnp.linalg.norm(L),
                        "energy": E,
                        "virial": Vratio,
                        "imbalance_abs": Iabs}

    # Record initial state first (must match hist dtypes/shapes)
    # imbalance uses max|I| per body — same statistic as body_fn below
    # (was ‖I‖₂ at t=0, inconsistent with per-tick max; audit fix 2026-10-07)
    L0 = compute_angular_momentum(state_0)
    I0 = compute_imbalance(state_0)
    init_hist = {
        "L_norm": jnp.array([jnp.linalg.norm(L0)]),
        "energy": jnp.array([compute_total_energy(state_0, G)]),
        "virial": jnp.array([compute_virial_ratio(state_0, G)]),
        "imbalance_abs": jnp.array([jnp.max(jnp.abs(I0))]),  # scalar, matches hist
    }

    _, hist = lax.scan(body_fn, state_0, jnp.arange(n_ticks))

    # Concatenate initial + subsequent
    return (
        jnp.concatenate([init_hist["L_norm"], hist["L_norm"]]),
        jnp.concatenate([init_hist["energy"], hist["energy"]]),
        jnp.concatenate([init_hist["virial"], hist["virial"]]),
        jnp.concatenate([init_hist["imbalance_abs"], hist["imbalance_abs"]]),
    )


# ------------------------------------------------------------------
# Convenience: build state from raw L2 slice
# ------------------------------------------------------------------

def state_from_l2(bids_0: jnp.ndarray,
                  asks_0: jnp.ndarray,
                  bids_1: jnp.ndarray,
                  asks_1: jnp.ndarray,
                  bids_2: jnp.ndarray,
                  asks_2: jnp.ndarray) -> ThreeBodyState:
    """Construct ThreeBodyState from three L2 books (one per body / asset).

    Each book is a (K, 2) array of [price, quantity] levels (K ≤ 20 per
    DataSpec.md).  Mass and microprice follow Concept.md §2.2–2.3.

    Returns
    -------
    state : ThreeBodyState
        Ready for integration.
    """
    def _safe_sum_col(arr: jnp.ndarray, col: int) -> float:
        """Sum a column safely, returning 0 for empty arrays."""
        if arr.shape[0] == 0:
            return 0.0
        return jnp.sum(arr[:, col])

    def _microprice(bids: jnp.ndarray, asks: jnp.ndarray) -> float:
        q_b = _safe_sum_col(bids, 1) if bids.shape[0] > 0 else 0.0
        p_b = _safe_sum_col(bids, 0) if bids.shape[0] > 0 else 0.0
        q_a = _safe_sum_col(asks, 1) if asks.shape[0] > 0 else 0.0
        p_a = _safe_sum_col(asks, 0) if asks.shape[0] > 0 else 0.0
        q_tot = q_b + q_a
        # microprice = (q_a·p_b + q_b·p_a) / (q_b + q_a)
        if q_tot < EPSILON:
            return 0.0
        num = q_a * p_b + q_b * p_a
        return jnp.log(num / q_tot)

    def _mass(bids: jnp.ndarray, asks: jnp.ndarray) -> float:
        q_b = _safe_sum_col(bids, 1) if bids.shape[0] > 0 else 0.0
        q_a = _safe_sum_col(asks, 1) if asks.shape[0] > 0 else 0.0
        q_tot = q_b + q_a
        return jnp.log(1.0 + q_tot)

    def _imbalance(bids: jnp.ndarray, asks: jnp.ndarray) -> float:
        q_b = _safe_sum_col(bids, 1) if bids.shape[0] > 0 else 0.0
        q_a = _safe_sum_col(asks, 1) if asks.shape[0] > 0 else 0.0
        denom = q_b + q_a
        if denom < EPSILON:
            return 0.0
        return (q_b - q_a) / denom

    def _gamma(bids: jnp.ndarray, asks: jnp.ndarray,
               microprice: float) -> float:
        if bids.shape[0] == 0 or asks.shape[0] == 0:
            return 0.0
        spread = asks[0, 0] - bids[0, 0]
        if jnp.abs(microprice) < EPSILON:
            return 0.0
        return spread / microprice

    x0 = _microprice(bids_0, asks_0)
    x1 = _microprice(bids_1, asks_1)
    x2 = _microprice(bids_2, asks_2)

    m0 = _mass(bids_0, asks_0)
    m1 = _mass(bids_1, asks_1)
    m2 = _mass(bids_2, asks_2)

    I0 = _imbalance(bids_0, asks_0)
    I1 = _imbalance(bids_1, asks_1)
    I2 = _imbalance(bids_2, asks_2)

    g0 = _gamma(bids_0, asks_0, x0)
    g1 = _gamma(bids_1, asks_1, x1)
    g2 = _gamma(bids_2, asks_2, x2)

    x = jnp.stack([x0, x1, x2])
    v = jnp.zeros(3)          # start from rest (tick 0)
    m = jnp.stack([m0, m1, m2])
    I = jnp.stack([I0, I1, I2])
    gamma = jnp.stack([g0, g1, g2])

    return ThreeBodyState(x=x, v=v, m=m, I=I, gamma=gamma)
