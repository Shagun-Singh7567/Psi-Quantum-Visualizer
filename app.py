"""
app.py — Psi · Hydrogen Orbital Viewer

Layout
------
Row 1 : radial R(r) | angular |Y|²          (two equal columns, 380px)
Row 2 : XZ / XY / YZ heatmaps in st.tabs   (three equal columns, 360px)
Row 3 : radial probability P(r)             (full width, 220px)
Row 4 : 3D volume expander
"""

import numpy as np
import streamlit as st

import hydrogen
import plots
from theme import inject_css, metric_html, orbital_table_html, Font, Color

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Psi · Hydrogen Orbital Viewer",
    page_icon="ψ",
    layout="wide",
)
inject_css()

L_LABELS = {0: "s", 1: "p", 2: "d"}

# ── Cached compute functions ──────────────────────────────────────────────────

@st.cache_data
def compute_orbital(n, l, m):
    r_a0, R_vals      = hydrogen.radial_plot_data(n, l)
    ang_x, ang_y      = hydrogen.angular_polar_data(l, m)
    r_mean            = hydrogen.mean_radius(n, l)
    r_nodes_count     = hydrogen.radial_nodes(n, l)
    a_nodes_count     = hydrogen.angular_nodes(l)
    r_a0_fine, R_fine = hydrogen.radial_plot_data(n, l, n_points=600)
    P_r               = r_a0_fine ** 2 * R_fine ** 2
    return (r_a0, R_vals, ang_x, ang_y,
            r_mean, r_nodes_count, a_nodes_count, r_a0_fine, P_r)

@st.cache_data
def compute_plane(n, l, m, plane):
    return hydrogen.orbital_2d_grid_plane(n, l, m, plane=plane, grid_size=250)

@st.cache_data
def compute_volume(n, l, m):
    return plots.volume_3d_figure(n, l, m)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="psi-title">ψ &nbsp; Psi — Hydrogen Orbital Viewer</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="psi-sub">'
    'Exact analytic solutions &nbsp;·&nbsp; '
    'radial &nbsp;·&nbsp; angular &nbsp;·&nbsp; '
    '|ψ|² cross-sections &nbsp;·&nbsp; 3D volume'
    '</div>',
    unsafe_allow_html=True,
)

# ── Controls card ─────────────────────────────────────────────────────────────
st.markdown('<div class="controls-card">', unsafe_allow_html=True)

qn1, qn2, qn3, _ = st.columns([2, 3, 4, 3])

with qn1:
    st.markdown('<div class="qn-label">Principal &nbsp;(n)</div>',
                unsafe_allow_html=True)
    n = st.radio("n", options=[1, 2, 3], horizontal=True,
                 label_visibility="collapsed")

with qn2:
    l_options = list(range(n))
    l_labels  = [f"{v} ({L_LABELS[v]})" for v in l_options]
    st.markdown('<div class="qn-label">Angular &nbsp;(l)</div>',
                unsafe_allow_html=True)
    l_label = st.radio("l", options=l_labels, horizontal=True,
                       label_visibility="collapsed")
    l = l_options[l_labels.index(l_label)]

with qn3:
    m_options = list(range(-l, l + 1))
    st.markdown('<div class="qn-label">Magnetic &nbsp;(m)</div>',
                unsafe_allow_html=True)
    m = st.radio("m", options=m_options, horizontal=True,
                 label_visibility="collapsed")

st.markdown(
    '<div class="orbital-name">'
    + str(n) + L_LABELS.get(l, "?")
    + ' &nbsp;(m = ' + str(m) + ')'
    + '</div>',
    unsafe_allow_html=True,
)

st.markdown('</div>', unsafe_allow_html=True)

# ── Physics ───────────────────────────────────────────────────────────────────
(r_a0, R_vals, ang_x, ang_y,
 r_mean, r_nodes_count, a_nodes_count, r_a0_fine, P_r) = compute_orbital(n, l, m)

# ── Metrics row ───────────────────────────────────────────────────────────────
mc1, mc2, mc3, mc4 = st.columns(4)
with mc1:
    st.markdown(metric_html("Orbital", str(n) + L_LABELS.get(l, "?")),
                unsafe_allow_html=True)
with mc2:
    st.markdown(metric_html("⟨r⟩", str(round(r_mean, 1)) + " a₀"),
                unsafe_allow_html=True)
with mc3:
    st.markdown(metric_html("Radial nodes", str(r_nodes_count)),
                unsafe_allow_html=True)
with mc4:
    st.markdown(metric_html("Angular nodes", str(a_nodes_count)),
                unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1 — radial and angular ────────────────────────────────────────────────
col_r, col_ang = st.columns([1, 1])

with col_r:
    st.plotly_chart(
        plots.radial_figure(r_a0, R_vals, n, l),
        use_container_width=True,
    )

with col_ang:
    st.plotly_chart(
        plots.angular_figure(ang_x, ang_y, l, m),
        use_container_width=True,
    )

# ── Row 2 — cross-section heatmaps in tabs ────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div class="section-gap"></div>',
    unsafe_allow_html=True,
)

tab_xz, tab_xy, tab_yz = st.tabs([
    "XZ &nbsp; (standard)",
    "XY &nbsp; (equatorial)",
    "YZ &nbsp; (side)",
])

with tab_xz:
    A, B, psi2, extent, xlabel, ylabel = compute_plane(n, l, m, "xz")
    st.plotly_chart(
        plots.heatmap_figure(A, B, psi2, extent, n, l, m, "xz", xlabel, ylabel),
        use_container_width=True,
    )
    st.caption(
        "XZ cross-section (y=0). The standard chemistry view — "
        "z is the quantisation axis."
    )

with tab_xy:
    A, B, psi2, extent, xlabel, ylabel = compute_plane(n, l, m, "xy")
    st.plotly_chart(
        plots.heatmap_figure(A, B, psi2, extent, n, l, m, "xy", xlabel, ylabel),
        use_container_width=True,
    )
    st.caption(
        "XY cross-section (z=0). Equatorial slice — "
        "shows azimuthal structure for m≠0 orbitals."
    )

with tab_yz:
    A, B, psi2, extent, xlabel, ylabel = compute_plane(n, l, m, "yz")
    st.plotly_chart(
        plots.heatmap_figure(A, B, psi2, extent, n, l, m, "yz", xlabel, ylabel),
        use_container_width=True,
    )
    st.caption(
        "YZ cross-section (x=0). Side view — "
        "complementary to XZ for non-symmetric orbitals."
    )

# ── Row 3 — radial probability ────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "#### Radial probability &nbsp; P(r) = r² |R(r)|²",
    unsafe_allow_html=True,
)
st.plotly_chart(
    plots.radial_prob_figure(r_a0_fine, P_r, r_mean),
    use_container_width=True,
)
st.caption(
    "Probability of finding the electron at radius r regardless of angle. "
    "Dashed line marks ⟨r⟩. Peak count = radial nodes + 1."
)

# ── Row 4 — 3D volume ─────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("🔬  3D orbital volume  (interactive · drag to rotate)"):
    st.caption(
        "Full opacity cloud of |ψ|² as a Plotly Volume trace. "
        "Grid scales with n — d orbitals use a finer grid and may take "
        "a few seconds on first render."
    )
    st.plotly_chart(
        compute_volume(n, l, m),
        use_container_width=True,
    )

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<span style="font-family:' + Font.MONO + '; font-size:0.75rem;'
        ' font-weight:700; color:' + Color.TEXT_MUTED + '; text-transform:uppercase;'
        ' letter-spacing:0.12em;">Orbital guide</span>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(orbital_table_html(n, l, m), unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        '<div class="sidebar-caption">'
        'ψ<sub>nlm</sub> = R<sub>nl</sub>(r) · Y<sub>l</sub><sup>m</sup>(θ,φ)'
        '<br><br>'
        'Exact solutions via SciPy special functions.<br>'
        'n = 1, 2, 3 &nbsp;·&nbsp; l = 0 … n−1 &nbsp;·&nbsp; m = −l … l'
        '</div>',
        unsafe_allow_html=True,
    )