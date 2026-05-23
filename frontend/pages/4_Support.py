"""AI Support — 20 agents, chat, audit trail, HITL."""
import time

import streamlit as st

from agents_registry import SAMPLE_QUERIES_BY_CATEGORY
from api_client import post_chat
from layout import apply_theme, init_session, render_footer, render_navbar, require_profile
from scene_3d import render_3d_scene
from ui_components import (
    render_agent_grid,
    render_agent_pipeline,
    render_ai_response,
    render_booking_summary,
    render_chat_bubble,
    render_escalation,
    render_hitl_card,
    render_metrics,
    render_recommendations,
)

st.set_page_config(page_title="AI Support", page_icon="💬", layout="wide")
init_session()
require_profile()
apply_theme()
render_navbar()

if "pending_query" in st.session_state:
    pq = st.session_state.pending_query
    del st.session_state.pending_query
    st.session_state.messages.append({"role": "user", "content": pq})
    st.session_state.last_result = post_chat(pq, st.session_state.booking_id or None)
    st.session_state.messages.append({"role": "assistant", "content": st.session_state.last_result.get("response", "")})

render_3d_scene(st.session_state.theme, 180, scene="support", node_count=20)

with st.sidebar:
    st.markdown("#### Sample queries (Section 10)")
    for cat, queries in SAMPLE_QUERIES_BY_CATEGORY.items():
        st.caption(f"**{cat}**")
        for i, q in enumerate(queries):
            if st.button(q[:46] + "…", key=f"sq_{cat}_{i}", use_container_width=True):
                st.session_state.pending_query = q
                st.rerun()
    st.text_input("Booking ID", key="booking_id")

chat_col, agent_col = st.columns([1.3, 1])
with chat_col:
    st.markdown('<div class="tw-card-title">TripWise AI — 20 Agent Orchestration</div>', unsafe_allow_html=True)
    box = st.container(height=320, border=True)
    with box:
        if not st.session_state.messages:
            st.markdown(
                '<div class="tw-chat-ai">🤖 Namaste! Ask about bookings, refunds, delays, baggage, '
                'hotels, packages, or "find cheapest DEL to Dubai".</div>',
                unsafe_allow_html=True,
            )
        for msg in st.session_state.messages:
            render_chat_bubble(msg["role"], msg["content"])
    ic1, ic2 = st.columns([4, 1])
    with ic1:
        inp = st.text_input("Message", label_visibility="collapsed", key="support_input")
    with ic2:
        send = st.button("Send ✈", use_container_width=True)
    if send and inp.strip():
        st.session_state.messages.append({"role": "user", "content": inp.strip()})
        with st.spinner("20 agents collaborating…"):
            time.sleep(0.5)
            st.session_state.last_result = post_chat(inp.strip(), st.session_state.booking_id or None)
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.last_result.get("response", "")})
        st.rerun()
    result = st.session_state.last_result
    if result:
        render_metrics(result.get("intent", ""), float(result.get("confidence", 0)), result.get("escalate", False), result.get("mode", "mock"))
        if result.get("escalate"):
            render_escalation(result.get("escalation_reason", ""))
            render_hitl_card(result)
        render_ai_response(result.get("response", ""))
        render_recommendations(result.get("recommendations", []))
        if result.get("flight_options"):
            st.dataframe(
                [{"Airline": f"{x['airline']} {x['flight_no']}", "Price": x["price_inr"], "Dep": x["dep"]} for x in result["flight_options"][:5]],
                use_container_width=True,
            )
        with st.expander("Audit trail (capstone deliverable #9)"):
            st.write("Intent:", result.get("intent"))
            st.write("Active agents:", result.get("agents_active", []))
            st.write("Sources:", result.get("sources", []))
            st.json(result.get("agents_trace", []))

with agent_col:
    result = st.session_state.last_result or {}
    st.markdown("#### Agent Command Center")
    render_agent_grid(result.get("agents_active", []))
    render_agent_pipeline(result.get("agents_trace", []))
    if result.get("booking_summary"):
        render_booking_summary(result["booking_summary"])

render_footer()
