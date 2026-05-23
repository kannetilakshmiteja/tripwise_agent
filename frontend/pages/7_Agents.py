"""AI Agents catalog — clean row layout by category."""
import html

import streamlit as st

from agents_registry import AGENT_SAMPLE_QUERIES, AGENTS, AGENT_CATEGORIES
from layout import apply_theme, init_session, render_footer, render_navbar, require_profile

BORDER_COLORS = {
    "Booking": "#0077b6",
    "Refund & Cancel": "#dc2626",
    "Disruption": "#d97706",
    "Hotel": "#7c3aed",
    "Flight": "#0284c7",
    "Policy": "#64748b",
    "Payment": "#059669",
    "General": "#e85d04",
}

st.set_page_config(page_title="AI Agents", page_icon="🤖", layout="wide")
init_session()
require_profile()
apply_theme()
render_navbar()

st.markdown('<div class="tw-agents-header">', unsafe_allow_html=True)
st.markdown(
    '<p style="margin:0 0 0.5rem;font-size:1rem"><b>How it works:</b> '
    "Intent → Specialist agent → Policy check → Response → Human escalation if needed.</p>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="tw-pipeline">'
    '<span class="tw-pipe-node">Intent</span> → '
    '<span class="tw-pipe-node">Specialist</span> → '
    '<span class="tw-pipe-node">Policy</span> → '
    '<span class="tw-pipe-node">Response</span> → '
    '<span class="tw-pipe-node tw-pipe-esc">Escalation</span>'
    "</div>",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

category = st.selectbox("Filter by category", AGENT_CATEGORIES, index=0)
filtered = AGENTS if category == "All" else [a for a in AGENTS if a.get("category") == category]
st.caption(f"{len(filtered)} agents")

for agent in filtered:
    cat = agent.get("category", "General")
    sample = AGENT_SAMPLE_QUERIES.get(agent["id"], f"Help with {agent['name']}")
    bc = BORDER_COLORS.get(cat, "#e85d04")
    row_l, row_r = st.columns([5, 1])
    with row_l:
        st.markdown(
            f'<div class="tw-agent-row" style="border-left-color:{bc}">'
            f'<div class="tw-agent-row-icon">{agent["icon"]}</div>'
            f'<div class="tw-agent-row-body">'
            f"<strong>{html.escape(agent['name'])}</strong> "
            f'<span class="tw-badge">{html.escape(cat)}</span><br/>'
            f"<span>{html.escape(agent['desc'])}</span><br/>"
            f'<span style="font-style:italic;font-size:0.75rem">e.g. {html.escape(sample[:70])}</span>'
            f"</div></div>",
            unsafe_allow_html=True,
        )
    with row_r:
        st.write("")
        st.write("")
        if st.button("Try", key=f"agent_try_{agent['id']}", use_container_width=True):
            st.session_state.pending_query = sample
            st.switch_page("pages/4_Support.py")

st.divider()
st.page_link("pages/4_Support.py", label="Open AI Support chat", icon="💬")

render_footer()
