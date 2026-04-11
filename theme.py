"""
theme.py — Psi design system, dark theme.

CSS built via plain string concatenation — no f-strings —
to avoid curly-brace conflicts between Python and CSS syntax.
"""

import streamlit as st


# ── Colors ────────────────────────────────────────────────────────────────────

class Color:
    BG_PAGE        = "#0e1117"
    BG_SURFACE     = "#161b22"
    BG_CARD        = "#1a2332"
    BG_TRANSPARENT = "rgba(0,0,0,0)"
    BG_DARK        = "#0a0a14"

    PRIMARY        = "#2dd4a0"
    PRIMARY_DIM    = "#1a8f6e"
    PRIMARY_GLOW   = "rgba(45,212,160,0.15)"
    DARK           = "#0e6e52"

    TEXT_BRIGHT    = "#e6edf3"
    TEXT_BODY      = "#c9d1d9"
    TEXT_MUTED     = "#6e7681"
    TEXT_FAINT     = "#3d4450"

    NODE           = "rgba(255, 220, 100, 0.55)"
    NODE_BORDER    = "rgba(255, 200, 50, 0.85)"

    BORDER         = "#21262d"
    AXIS           = "#30363d"
    ZERO_LINE      = "rgba(255,255,255,0.1)"
    MEAN_LINE      = "#f0883e"
    FILL           = "rgba(45,212,160,0.10)"

    HEATMAP = [
        [0.00, "#0a0a14"],
        [0.15, "#0F6E56"],
        [0.40, "#1D9E75"],
        [0.65, "#9FE1CB"],
        [0.85, "#E1F5EE"],
        [1.00, "#ffffff"],
    ]

    TABLE_HEADER        = "#1e2a3a"
    TABLE_ROW           = "#161b22"
    TABLE_ACTIVE        = "rgba(45,212,160,0.18)"
    TABLE_ACTIVE_BORDER = "#2dd4a0"


# ── Font ──────────────────────────────────────────────────────────────────────

class Font:
    BODY   = "Nunito, sans-serif"
    MONO   = "IBM Plex Mono, monospace"   # kept for metric values and orbital labels
    IMPORT = (
        "https://fonts.googleapis.com/css2?"
        "family=Nunito:wght@400;600;700&family=IBM+Plex+Mono:wght@400;700&display=swap"
    )


# ── Plotly layout template ────────────────────────────────────────────────────

def h_layout(title: str = "", dark: bool = False) -> dict:
    """Base Plotly layout for all hydrogen figures."""
    return dict(
        title=dict(
            text=title,
            font=dict(family=Font.BODY, size=13, color=Color.TEXT_BODY),
        ),
        font=dict(family=Font.BODY, size=12, color=Color.TEXT_BODY),
        paper_bgcolor=Color.BG_DARK if dark else Color.BG_SURFACE,
        plot_bgcolor=Color.BG_SURFACE,
        margin=dict(l=48, r=24, t=44, b=44),
        legend=dict(
            font=dict(family=Font.BODY, size=10, color=Color.TEXT_MUTED),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
        ),
    )


# ── CSS ───────────────────────────────────────────────────────────────────────

def _build_css() -> str:
    c = Color
    f = Font.BODY
    mono = Font.MONO

    return (
        '<link href="' + Font.IMPORT + '" rel="stylesheet">\n'
        "<style>\n"

        # ── Global dark background ────────────────────────────────────────────
        ".stApp {"
        "  background-color: " + c.BG_PAGE + " !important;"
        "}\n"

        # Global soft-white text
        ".stApp, .stApp p, .stApp span, .stApp div,"
        " .stApp label, .stApp li, .stApp td, .stApp th {"
        "  color: " + c.TEXT_BODY + " !important;"
        "}\n"

        "[data-testid='stMarkdownContainer'] p,"
        " [data-testid='stMarkdownContainer'] li,"
        " [data-testid='stMarkdownContainer'] span {"
        "  color: " + c.TEXT_BODY + " !important;"
        "}\n"

        # ── Sidebar ───────────────────────────────────────────────────────────
        "[data-testid='stSidebar'] {"
        "  background-color: " + c.BG_SURFACE + " !important;"
        "  border-right: 1px solid " + c.BORDER + ";"
        "}\n"

        "[data-testid='stSidebar'] * {"
        "  color: " + c.TEXT_BODY + " !important;"
        "}\n"

        # ── Page header ───────────────────────────────────────────────────────
        ".psi-title {"
        "  font-family: " + f + ";"
        "  font-size: 2.4rem;"
        "  font-weight: 700;"
        "  letter-spacing: -1.5px;"
        "  color: " + c.PRIMARY + ";"
        "  margin-bottom: 2px;"
        "}\n"

        ".psi-sub {"
        "  font-family: " + f + ";"
        "  font-size: 0.78rem;"
        "  color: " + c.TEXT_FAINT + ";"
        "  margin-top: 0;"
        "  margin-bottom: 2rem;"
        "  letter-spacing: 0.02em;"
        "}\n"

        # ── Controls card ─────────────────────────────────────────────────────
        ".controls-card {"
        "  background: " + c.BG_CARD + ";"
        "  border: 1px solid " + c.BORDER + ";"
        "  border-radius: 10px;"
        "  padding: 1.2rem 1.4rem 1rem 1.4rem;"
        "  margin-bottom: 1.2rem;"
        "}\n"

        # ── Quantum number labels ─────────────────────────────────────────────
        ".qn-label {"
        "  font-family: " + f + ";"
        "  font-size: 0.65rem;"
        "  color: " + c.TEXT_MUTED + ";"
        "  text-transform: uppercase;"
        "  letter-spacing: 0.12em;"
        "  margin-bottom: 6px;"
        "}\n"

        # ── Orbital name badge ────────────────────────────────────────────────
        ".orbital-name {"
        "  font-family: " + mono + ";"
        "  font-size: 0.88rem;"
        "  color: " + c.PRIMARY + ";"
        "  background: " + c.PRIMARY_GLOW + ";"
        "  border-left: 3px solid " + c.PRIMARY + ";"
        "  border-radius: 0 6px 6px 0;"
        "  padding: 6px 16px;"
        "  display: inline-block;"
        "  margin-top: 0.6rem;"
        "  margin-bottom: 0.4rem;"
        "}\n"

        # ── Section spacing ───────────────────────────────────────────────────
        ".section-gap {"
        "  margin-top: 1.6rem;"
        "  margin-bottom: 0.4rem;"
        "}\n"

        # ── Metric boxes ──────────────────────────────────────────────────────
        ".metric-box {"
        "  background: " + c.BG_CARD + ";"
        "  border: 1px solid " + c.BORDER + ";"
        "  border-left: 3px solid " + c.PRIMARY + ";"
        "  border-radius: 0 8px 8px 0;"
        "  padding: 0.85rem 1.1rem;"
        "  font-family: " + f + ";"
        "  transition: box-shadow 0.2s ease, border-color 0.2s ease;"
        "  cursor: default;"
        "}\n"

        ".metric-box:hover {"
        "  box-shadow: 0 0 0 1px " + c.PRIMARY_DIM + ","
        "              0 0 12px 0 rgba(45,212,160,0.2);"
        "  border-left-color: " + c.PRIMARY + ";"
        "}\n"

        ".metric-lbl {"
        "  font-size: 0.66rem;"
        "  color: " + c.TEXT_MUTED + ";"
        "  text-transform: uppercase;"
        "  letter-spacing: 0.09em;"
        "  margin-bottom: 4px;"
        "}\n"

        ".metric-val {"
        "  font-size: 1.6rem;"
        "  font-weight: 700;"
        "  font-family: " + mono + ";"
        "  color: " + c.TEXT_BRIGHT + ";"
        "  line-height: 1.1;"
        "}\n"

        # ── Chart container hover glow ────────────────────────────────────────
        "[data-testid='stPlotlyChart'] {"
        "  border-radius: 8px;"
        "  transition: box-shadow 0.2s ease;"
        "}\n"

        "[data-testid='stPlotlyChart']:hover {"
        "  box-shadow: 0 0 0 1px " + c.BORDER + ","
        "              0 0 16px 0 rgba(45,212,160,0.12);"
        "}\n"

        # ── Sidebar caption ───────────────────────────────────────────────────
        ".sidebar-caption {"
        "  font-size: 0.7rem;"
        "  color: " + c.TEXT_MUTED + ";"
        "  line-height: 1.7;"
        "  font-family: " + mono + ";"
        "}\n"

        # ── Orbital table ─────────────────────────────────────────────────────
        ".otbl {"
        "  width: 100%;"
        "  border-collapse: collapse;"
        "  font-family: " + mono + ";"
        "  font-size: 0.72rem;"
        "  margin-bottom: 10px;"
        "}\n"

        ".otbl-shell {"
        "  background: " + c.TABLE_HEADER + ";"
        "  color: " + c.TEXT_MUTED + ";"
        "  font-size: 0.6rem;"
        "  text-transform: uppercase;"
        "  letter-spacing: 0.1em;"
        "  padding: 5px 8px;"
        "  border-top: 1px solid " + c.BORDER + ";"
        "}\n"

        ".otbl td {"
        "  padding: 5px 8px;"
        "  color: " + c.TEXT_MUTED + ";"
        "  background: " + c.TABLE_ROW + ";"
        "  border-bottom: 1px solid " + c.BORDER + ";"
        "  text-align: center;"
        "  white-space: nowrap;"
        "  transition: background 0.15s ease;"
        "}\n"

        ".otbl td.active {"
        "  color: " + c.PRIMARY + ";"
        "  background: " + c.TABLE_ACTIVE + ";"
        "  border-left: 2px solid " + c.TABLE_ACTIVE_BORDER + ";"
        "  font-weight: 700;"
        "}\n"

        ".otbl td.lbl {"
        "  color: " + c.TEXT_FAINT + ";"
        "  font-size: 0.6rem;"
        "  text-transform: uppercase;"
        "  letter-spacing: 0.08em;"
        "  text-align: left;"
        "  background: " + c.TABLE_ROW + ";"
        "  border: none;"
        "  padding-right: 10px;"
        "}\n"

        # ── Divider ───────────────────────────────────────────────────────────
        "hr { border-color: " + c.BORDER + "; }\n"

        # ── Radio + toggle labels ─────────────────────────────────────────────
        # ── Radio buttons — pill style ────────────────────────────────────
        # Hide the native dot indicator
        ".stRadio [data-testid='stMarkdownContainer'] p {"
        "  font-family: " + f + ";"
        "  font-size: 0.82rem;"
        "}\n"

        ".stRadio > div {"
        "  gap: 6px !important;"
        "}\n"

        # Each radio option wrapper
        ".stRadio label {"
        "  background: " + c.BG_CARD + " !important;"
        "  border: 1px solid " + c.BORDER + " !important;"
        "  border-radius: 6px !important;"
        "  padding: 4px 14px !important;"
        "  font-family: " + f + " !important;"
        "  font-size: 0.82rem !important;"
        "  color: " + c.TEXT_MUTED + " !important;"
        "  cursor: pointer !important;"
        "  transition: all 0.15s ease !important;"
        "}\n"

        # Hide the dot circle entirely
        ".stRadio label > div:first-child {"
        "  display: none !important;"
        "}\n"

        # Checked state — teal pill
        ".stRadio label[data-checked='true'] {"
        "  background: " + c.PRIMARY_GLOW + " !important;"
        "  border-color: " + c.PRIMARY + " !important;"
        "  color: " + c.PRIMARY + " !important;"
        "}\n"

        # Hover on unselected
        ".stRadio label:hover {"
        "  border-color: " + c.PRIMARY_DIM + " !important;"
        "  color: " + c.TEXT_BODY + " !important;"
        "}\n"

        ".stCheckbox label {"
        "  color: " + c.TEXT_BODY + " !important;"
        "  font-family: " + f + ";"
        "}\n"

        # ── Section headers ───────────────────────────────────────────────────
        "h4 { color: " + c.TEXT_BRIGHT + " !important; }\n"

        # ── Captions ─────────────────────────────────────────────────────────
        ".stCaption, [data-testid='stCaptionContainer'] {"
        "  color: " + c.TEXT_MUTED + " !important;"
        "}\n"

        # ── Tabs ─────────────────────────────────────────────────────────────
        ".stTabs [data-baseweb='tab-list'] {"
        "  background: " + c.BG_SURFACE + ";"
        "  border-bottom: 1px solid " + c.BORDER + ";"
        "  gap: 4px;"
        "}\n"

        ".stTabs [data-baseweb='tab'] {"
        "  font-family: " + f + ";"
        "  font-size: 0.78rem;"
        "  color: " + c.TEXT_MUTED + " !important;"
        "  background: transparent;"
        "  border-radius: 6px 6px 0 0;"
        "  padding: 6px 18px;"
        "}\n"

        ".stTabs [aria-selected='true'] {"
        "  color: " + c.PRIMARY + " !important;"
        "  border-bottom: 2px solid " + c.PRIMARY + " !important;"
        "  background: " + c.PRIMARY_GLOW + ";"
        "}\n"

        # ── Expander ─────────────────────────────────────────────────────────
        ".stExpander {"
        "  border: 1px solid " + c.BORDER + " !important;"
        "  border-radius: 8px !important;"
        "  background: " + c.BG_SURFACE + ";"
        "}\n"

        "div.stButton > button {"
        "  font-family: " + f + " !important;"
        "  background: " + c.BG_CARD + ";"
        "  border: 1px solid " + c.BORDER + ";"
        "  color: " + c.TEXT_BODY + ";"
        "  transition: box-shadow 0.2s ease;"
        "}\n"

        "div.stButton > button:hover {"
        "  box-shadow: 0 0 10px rgba(45,212,160,0.25);"
        "  border-color: " + c.PRIMARY_DIM + ";"
        "}\n"

        "</style>"
    )


_CSS = _build_css()


# ── Public API ────────────────────────────────────────────────────────────────

def inject_css() -> None:
    """Inject all Psi dark-theme styles into the current Streamlit page."""
    st.markdown(_CSS, unsafe_allow_html=True)


def metric_html(label: str, value: str) -> str:
    """Return HTML for a styled dark-theme metric box."""
    return (
        '<div class="metric-box">'
        '<div class="metric-lbl">' + label + '</div>'
        '<div class="metric-val">' + value + '</div>'
        '</div>'
    )


def orbital_table_html(n_active: int, l_active: int, m_active: int) -> str:
    """
    Compact HTML table grouping orbitals by shell (n=1..3).
    Active cell is highlighted with teal fill and border.
    """
    L_LABELS = {0: "s", 1: "p", 2: "d"}
    rows = '<table class="otbl">'

    for ni in range(1, 4):
        subshells = ", ".join(str(ni) + L_LABELS[li] for li in range(ni))
        rows += (
            '<tr><td colspan="20" class="otbl-shell">'
            'n = ' + str(ni) + ' &nbsp;·&nbsp; ' + subshells +
            '</td></tr>'
        )
        for li in range(ni):
            m_vals = list(range(-li, li + 1))
            lbl    = str(ni) + L_LABELS[li]
            rows  += '<tr>'
            rows  += '<td class="lbl">' + lbl + '</td>'
            for mi in m_vals:
                active = (ni == n_active and li == l_active and mi == m_active)
                cls    = 'active' if active else ''
                rows  += '<td class="' + cls + '">m=' + str(mi) + '</td>'
            rows += '</tr>'

    rows += '</table>'
    return rows