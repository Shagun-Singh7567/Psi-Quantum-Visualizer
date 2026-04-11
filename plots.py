"""
plots.py — Plotly figure builders for the Psi hydrogen orbital viewer.

All functions return go.Figure. No Streamlit calls here.

Public API
----------
radial_figure(r_a0, R_vals, n, l)
angular_figure(ang_x, ang_y, l, m)
heatmap_figure(A, B, psi2, extent, n, l, m, plane, xlabel, ylabel)
radial_prob_figure(r_a0, P_r, r_mean)
volume_3d_figure(n, l, m)
"""

import numpy as np
import plotly.graph_objects as go

from theme import Color, Font, h_layout


# ── Radial wavefunction ───────────────────────────────────────────────────────

def radial_figure(
    r_a0: np.ndarray,
    R_vals: np.ndarray,
    n: int,
    l: int,
) -> go.Figure:
    """Line + fill plot of R_{nl}(r) vs r."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=r_a0, y=R_vals,
        mode="lines",
        line=dict(color=Color.PRIMARY, width=2.5),
        fill="tozeroy",
        fillcolor=Color.FILL,
        name=f"R_{n}{l}(r)",
    ))
    fig.add_hline(y=0, line=dict(color=Color.AXIS, width=0.5))

    fig.update_layout(**h_layout(f"Radial  R_{n}{l}(r)"), height=380, showlegend=False)
    fig.update_layout(
        xaxis=dict(title="r (a₀)", showgrid=False, zeroline=False,
                   color=Color.TEXT_MUTED, tickfont=dict(color=Color.TEXT_MUTED)),
        yaxis=dict(title="R(r)", showgrid=False, zeroline=False,
                   color=Color.TEXT_MUTED, tickfont=dict(color=Color.TEXT_MUTED)),
    )
    return fig


# ── Angular polar plot ────────────────────────────────────────────────────────

def angular_figure(
    ang_x: np.ndarray,
    ang_y: np.ndarray,
    l: int,
    m: int,
) -> go.Figure:
    """Polar plot of |Y_{lm}(θ)|² as a Cartesian shape."""
    max_r = max(np.max(np.abs(ang_x)), np.max(np.abs(ang_y))) * 1.2 or 0.5

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ang_x, y=ang_y,
        mode="lines",
        fill="toself",
        fillcolor="rgba(45,212,160,0.18)",
        line=dict(color=Color.PRIMARY, width=2),
        name=f"|Y_{l}^{m}|²",
    ))
    fig.add_hline(y=0, line=dict(color=Color.AXIS, width=0.5, dash="dot"))
    fig.add_vline(x=0, line=dict(color=Color.AXIS, width=0.5, dash="dot"))

    fig.update_layout(**h_layout(f"Angular  |Y_{l}^{m}|²"), height=380, showlegend=False)
    fig.update_layout(
        xaxis=dict(range=[-max_r, max_r], showgrid=False, zeroline=False,
                   scaleanchor="y", tickfont=dict(color=Color.TEXT_MUTED)),
        yaxis=dict(range=[-max_r, max_r], showgrid=False, zeroline=False,
                   tickfont=dict(color=Color.TEXT_MUTED)),
    )
    return fig


# ── Heatmap — single plane ────────────────────────────────────────────────────

def heatmap_figure(
    A: np.ndarray,
    B: np.ndarray,
    psi2: np.ndarray,
    extent: list,
    n: int,
    l: int,
    m: int,
    plane: str,
    xlabel: str,
    ylabel: str,
) -> go.Figure:
    """
    Dark-background heatmap of |ψ_{nlm}|² for one cross-section plane.

    Parameters
    ----------
    A, B         : coordinate grids (a₀) for the two free axes
    psi2         : probability density on the grid
    extent       : [amin, amax, bmin, bmax] in a₀
    n, l, m      : quantum numbers (for title)
    plane        : "xz" | "xy" | "yz" (for title)
    xlabel/ylabel: axis label strings returned by orbital_2d_grid_plane
    """
    psi2_display = np.log1p(psi2 / (psi2.max() + 1e-30) * 200)

    plane_label = plane.upper()
    title = f"|ψ_{n}{l}^{m}|²  {plane_label} cross-section"

    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        z=psi2_display,
        x=np.linspace(extent[0], extent[1], psi2.shape[1]),
        y=np.linspace(extent[2], extent[3], psi2.shape[0]),
        colorscale=Color.HEATMAP,
        showscale=False,
        hovertemplate=(
            xlabel.split(" ")[0] + "=%{x:.1f} a₀<br>"
            + ylabel.split(" ")[0] + "=%{y:.1f} a₀<extra></extra>"
        ),
    ))

    fig.add_hline(y=0, line=dict(color=Color.ZERO_LINE, width=0.5))
    fig.add_vline(x=0, line=dict(color=Color.ZERO_LINE, width=0.5))

    fig.update_layout(
        **h_layout(title, dark=True),
        height=360,
        showlegend=False,
    )
    fig.update_layout(
        xaxis=dict(title=xlabel, showgrid=False, zeroline=False,
                   tickfont=dict(color=Color.TEXT_MUTED, size=10)),
        yaxis=dict(title=ylabel, showgrid=False, zeroline=False,
                   scaleanchor="x",
                   tickfont=dict(color=Color.TEXT_MUTED, size=10)),
    )
    return fig


# ── Radial probability distribution ──────────────────────────────────────────

def radial_prob_figure(
    r_a0: np.ndarray,
    P_r: np.ndarray,
    r_mean: float,
) -> go.Figure:
    """P(r) = r²|R(r)|² with ⟨r⟩ marker."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=r_a0, y=P_r,
        mode="lines",
        line=dict(color=Color.PRIMARY, width=2),
        fill="tozeroy",
        fillcolor="rgba(45,212,160,0.12)",
        name="P(r)",
    ))
    fig.add_vline(
        x=r_mean,
        line=dict(color=Color.MEAN_LINE, width=1.5, dash="dash"),
        annotation_text=f"⟨r⟩ = {r_mean:.1f} a₀",
        annotation_font=dict(color=Color.MEAN_LINE, family=Font.MONO, size=11),
    )

    fig.update_layout(**h_layout(), height=220, showlegend=False)
    fig.update_layout(
        xaxis=dict(title="r (a₀)", showgrid=False, zeroline=False,
                   tickfont=dict(color=Color.TEXT_MUTED)),
        yaxis=dict(title="P(r)", showgrid=False, zeroline=False,
                   tickfont=dict(color=Color.TEXT_MUTED)),
    )
    return fig


# ── 3D volume ─────────────────────────────────────────────────────────────────

def volume_3d_figure(n: int, l: int, m: int) -> go.Figure:
    """
    Full opacity cloud of |ψ_{nlm}|² as a Plotly Volume trace.

    Grid size scales with n to maintain detail on d orbitals:
      n=1 → 35³, n=2 → 40³, n=3 → 55³
    """
    import hydrogen as hy

    grid_size = {1: 35, 2: 40, 3: 55}.get(n, 40)
    limit     = max(4, n * n * 6)
    coords    = np.linspace(-limit, limit, grid_size)
    X3, Y3, Z3 = np.meshgrid(coords, coords, coords)

    r     = np.sqrt(X3**2 + Y3**2 + Z3**2) * A0
    theta = np.arctan2(np.sqrt(X3**2 + Y3**2), Z3)
    phi   = np.arctan2(Y3, X3)

    R    = hy.radial_wavefunction(n, l, r)
    Yf   = hy.angular_wavefunction(l, m, theta, phi)
    psi2 = (R * Yf) ** 2
    val  = psi2 / (psi2.max() + 1e-30)

    fig = go.Figure(data=go.Volume(
        x=X3.flatten(),
        y=Y3.flatten(),
        z=Z3.flatten(),
        value=val.flatten(),
        isomin=0.001,
        isomax=1.0,
        opacity=0.08,
        surface_count=25,
        colorscale=Color.HEATMAP,
        showscale=False,
        caps=dict(x_show=False, y_show=False, z_show=False),
        hoverinfo="skip",
    ))

    fig.update_layout(
        **h_layout(f"|ψ_{n}{l}^{m}|²  3D volume", dark=True),
        height=500,
    )
    fig.update_layout(
        scene=dict(
            bgcolor=Color.BG_DARK,
            xaxis=dict(title="x (a₀)", showgrid=False,
                       backgroundcolor=Color.BG_DARK,
                       tickfont=dict(family=Font.MONO, size=9,
                                     color=Color.TEXT_MUTED)),
            yaxis=dict(title="y (a₀)", showgrid=False,
                       backgroundcolor=Color.BG_DARK,
                       tickfont=dict(family=Font.MONO, size=9,
                                     color=Color.TEXT_MUTED)),
            zaxis=dict(title="z (a₀)", showgrid=False,
                       backgroundcolor=Color.BG_DARK,
                       tickfont=dict(family=Font.MONO, size=9,
                                     color=Color.TEXT_MUTED)),
            camera=dict(eye=dict(x=1.4, y=1.4, z=1.0)),
        ),
        margin=dict(l=0, r=0, t=44, b=0),
    )
    return fig


# ── Module-level constant needed by volume_3d_figure ─────────────────────────
from constants import A0