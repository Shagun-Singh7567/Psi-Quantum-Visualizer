"""
hydrogen.py — Hydrogen atom wavefunction physics engine.

Uses SciPy special functions for exact analytic solutions.
No Streamlit, no Plotly — pure physics.

Public API
----------
radial_wavefunction(n, l, r)                    -> ndarray
angular_wavefunction(l, m, theta, phi)          -> ndarray
orbital_2d_grid_plane(n, l, m, plane, grid_sz)  -> A, B, psi2, extent
radial_plot_data(n, l, r_max_a0, n_pts)         -> r_a0, R
angular_polar_data(l, m, n_points)              -> x, y
mean_radius(n, l)                               -> float
radial_nodes(n, l)                              -> int
angular_nodes(l)                                -> int
"""

import numpy as np
from scipy.special import genlaguerre, factorial
from constants import A0

try:
    from scipy.special import sph_harm
except ImportError:
    from scipy.special import sph_harm_y as _y
    def sph_harm(m, l, phi, theta):
        return _y(l, m, theta, phi)


# ── Core wavefunctions ────────────────────────────────────────────────────────

def radial_wavefunction(n: int, l: int, r: np.ndarray) -> np.ndarray:
    """
    Normalised radial wavefunction R_{nl}(r).

    Parameters
    ----------
    n : principal quantum number (1, 2, 3)
    l : angular momentum quantum number (0 .. n-1)
    r : radial distance array in metres

    Returns
    -------
    R : radial wavefunction values (a₀^{-3/2})
    """
    rho  = 2.0 * r / (n * A0)
    norm = np.sqrt(
        (2.0 / (n * A0)) ** 3
        * factorial(n - l - 1)
        / (2 * n * factorial(n + l) ** 3)
    )
    L = genlaguerre(n - l - 1, 2 * l + 1)
    return norm * np.exp(-rho / 2) * rho ** l * L(rho)


def angular_wavefunction(
    l: int,
    m: int,
    theta: np.ndarray,
    phi: np.ndarray | float = 0.0,
) -> np.ndarray:
    """
    Real-valued angular wavefunction Y_{lm}(θ, φ).

    phi can be a scalar (fixed plane) or an ndarray matching theta
    (full grid dependence for XY / YZ planes).

    Returns the real ±m combination giving chemistry lobe shapes.
    """
    Y = sph_harm(abs(m), l, phi, theta)
    if m > 0:
        return np.real(Y) * np.sqrt(2)
    elif m < 0:
        return np.imag(Y) * np.sqrt(2)
    else:
        return np.real(Y)


# ── 2D cross-section grid ─────────────────────────────────────────────────────

def orbital_2d_grid_plane(
    n: int,
    l: int,
    m: int,
    plane: str = "xz",
    grid_size: int = 250,
):
    """
    |ψ_{nlm}|² on a 2D Cartesian cross-section through the origin.

    Parameters
    ----------
    n, l, m   : quantum numbers
    plane     : "xz" | "xy" | "yz"
    grid_size : points per axis

    Physics notes
    -------------
    All three planes pass through the origin.
    θ (polar, from z-axis) and φ (azimuthal, from x-axis) are computed
    correctly per grid point — φ is not fixed, so m≠0 orbitals show
    their full angular dependence on each slice.

    XZ plane  (y=0): free axes are x, z.
              r = √(x²+z²), θ = arctan2(|x|, z), φ = arctan2(0, x) → 0 or π
    XY plane  (z=0): free axes are x, y.
              r = √(x²+y²), θ = π/2 (equatorial), φ = arctan2(y, x)
    YZ plane  (x=0): free axes are y, z.
              r = √(y²+z²), θ = arctan2(|y|, z), φ = π/2 (y>0) or −π/2 (y<0)

    Returns
    -------
    A, B   : coordinate grids for the two free axes (a₀)
    psi2   : |ψ|² on the grid
    extent : [amin, amax, bmin, bmax] in a₀
    labels : (xlabel, ylabel) strings for plot axes
    """
    limit  = max(4, n * n * 6)              # adaptive box in a₀
    coords = np.linspace(-limit, limit, grid_size) * A0
    A_m, B_m = np.meshgrid(coords, coords)  # in metres

    if plane == "xz":
        # A = x, B = z
        x, z = A_m, B_m
        r     = np.sqrt(x**2 + z**2)
        theta = np.arctan2(np.abs(x), z)     # polar angle from z-axis
        phi   = np.arctan2(0.0, x)           # 0 for x>0, π for x<0
        xlabel, ylabel = "x (a₀)", "z (a₀)"

    elif plane == "xy":
        # A = x, B = y  — equatorial slice, z=0
        x, y  = A_m, B_m
        r     = np.sqrt(x**2 + y**2)
        theta = np.full_like(r, np.pi / 2)   # always equatorial
        phi   = np.arctan2(y, x)             # full azimuthal dependence
        xlabel, ylabel = "x (a₀)", "y (a₀)"

    elif plane == "yz":
        # A = y, B = z  — x=0 slice
        y, z  = A_m, B_m
        r     = np.sqrt(y**2 + z**2)
        theta = np.arctan2(np.abs(y), z)
        phi   = np.where(y >= 0, np.pi / 2, -np.pi / 2)
        xlabel, ylabel = "y (a₀)", "z (a₀)"

    else:
        raise ValueError("plane must be 'xz', 'xy', or 'yz'")

    R    = radial_wavefunction(n, l, r)
    Y    = angular_wavefunction(l, m, theta, phi)
    psi2 = (R * Y) ** 2

    extent = [-limit, limit, -limit, limit]
    A_a0   = A_m / A0
    B_a0   = B_m / A0

    return A_a0, B_a0, psi2, extent, xlabel, ylabel


# ── Plot data helpers ─────────────────────────────────────────────────────────

def radial_plot_data(n: int, l: int, r_max_a0: float = None, n_points: int = 400):
    """r (a₀) and R_{nl}(r) for a radial line plot."""
    if r_max_a0 is None:
        r_max_a0 = max(20, n * n * 8)
    r = np.linspace(0.01 * A0, r_max_a0 * A0, n_points)
    R = radial_wavefunction(n, l, r)
    return r / A0, R


def angular_polar_data(l: int, m: int, n_points: int = 360):
    """
    (x, y) of |Y_{lm}(θ)|² in polar form for a 2D polar plot.
    x = |Y|² sinθ,  y = |Y|² cosθ, mirrored onto both sides.
    """
    theta   = np.linspace(0, np.pi, n_points)
    Y       = angular_wavefunction(l, m, theta)
    r_polar = Y ** 2
    x = np.concatenate([ r_polar * np.sin(theta), -r_polar * np.sin(theta)])
    y = np.concatenate([ r_polar * np.cos(theta),  r_polar * np.cos(theta)])
    return x, y


# ── Derived quantities ────────────────────────────────────────────────────────

def mean_radius(n: int, l: int) -> float:
    """⟨r⟩ = a₀/2 · [3n² − l(l+1)] in Bohr radii."""
    return 0.5 * (3 * n ** 2 - l * (l + 1))


def radial_nodes(n: int, l: int) -> int:
    """Number of radial nodes = n − l − 1."""
    return n - l - 1


def angular_nodes(l: int) -> int:
    """Number of angular nodes = l."""
    return l