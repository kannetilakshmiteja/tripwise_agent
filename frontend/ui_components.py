"""Reusable HTML/UI helpers for Streamlit."""
import html
import streamlit as st


def hero_header(tagline: str) -> None:
    st.markdown(
        f"""
        <div class="tw-hero">
            <div class="tw-logo">✈ TripWise</div>
            <div class="tw-tagline">{html.escape(tagline)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def confidence_class(score: float) -> str:
    if score >= 0.75:
        return "tw-confidence-high"
    if score >= 0.6:
        return "tw-confidence-mid"
    return "tw-confidence-low"


def render_metrics(intent: str, confidence: float, escalate: bool, mode: str) -> None:
    c1, c2, c3, c4 = st.columns(4)
    conf_cls = confidence_class(confidence)
    esc_label = "Yes" if escalate else "No"
    esc_color = "danger" if escalate else "success"
    with c1:
        st.markdown(
            f'<div class="tw-metric"><div class="tw-metric-value">{intent.replace("_", " ").title()}</div>'
            f'<div class="tw-metric-label">Intent</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="tw-metric"><div class="tw-metric-value {conf_cls}">{confidence:.0%}</div>'
            f'<div class="tw-metric-label">Confidence</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="tw-metric"><div class="tw-metric-value" style="color:var(--esc)">'
            f'{esc_label}</div><div class="tw-metric-label">Escalation</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f'<div class="tw-metric"><div class="tw-metric-value" style="font-size:0.95rem">'
            f'{mode.upper()}</div><div class="tw-metric-label">Data Source</div></div>',
            unsafe_allow_html=True,
        )


def render_chat_bubble(role: str, content: str) -> None:
    safe = html.escape(content).replace("\n", "<br>")
    # Allow simple markdown bold from API
    safe = safe.replace("**", "").replace("*", "")
    cls = "tw-chat-user" if role == "user" else "tw-chat-ai"
    icon = "🧑" if role == "user" else "🤖"
    st.markdown(f'<div class="{cls}">{icon} {safe}</div>', unsafe_allow_html=True)


def render_escalation(reason: str) -> None:
    st.markdown(
        f"""
        <div class="tw-escalation">
            <strong>⚠ Escalated to Human Support</strong><br/>
            <span style="font-size:0.9rem">{html.escape(reason or "Low confidence or complex case")}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_booking_summary(summary: dict) -> None:
    if not summary:
        st.info("No booking summary in response.")
        return
    rows = [
        ("Booking ID", summary.get("booking_id", "—")),
        ("Customer", summary.get("customer_name", "—")),
        ("Route", summary.get("route", "—")),
        ("Flight", summary.get("flight", "—")),
        ("Departure", summary.get("departure", "—")),
        ("Hotel", summary.get("hotel", "—")),
        ("Status", summary.get("status", "—")),
        ("Payment", summary.get("payment_status", "—")),
        ("Amount", f"₹{summary.get('amount_inr', '—'):,}" if isinstance(summary.get("amount_inr"), (int, float)) else "—"),
        ("PNR", summary.get("pnr", "—")),
    ]
    inner = "".join(
        f'<div style="display:flex;justify-content:space-between;padding:0.35rem 0;border-bottom:1px solid rgba(128,128,128,0.15)">'
        f'<span style="opacity:0.7;font-size:0.85rem">{k}</span><strong style="font-size:0.85rem">{html.escape(str(v))}</strong></div>'
        for k, v in rows
    )
    st.markdown(
        f'<div class="tw-card"><div class="tw-card-title">📋 Booking Summary</div>{inner}</div>',
        unsafe_allow_html=True,
    )


def render_recommendations(recs: list) -> None:
    if not recs:
        return
    items = ""
    for r in recs:
        items += (
            f'<div class="tw-rec-item">'
            f'<strong>{html.escape(r.get("title", ""))}</strong><br/>'
            f'<span style="font-size:0.82rem;opacity:0.8">{html.escape(r.get("detail", ""))}</span>'
            f'</div>'
        )
    st.markdown(
        f'<div class="tw-card"><div class="tw-card-title">💡 Recommendations</div>{items}</div>',
        unsafe_allow_html=True,
    )


def render_agent_pipeline(trace: list) -> None:
    from agents_registry import AGENTS

    st.markdown('<div class="tw-card"><div class="tw-card-title">🧠 AI Agent Pipeline (20 Agents)</div>', unsafe_allow_html=True)
    trace_map = {}
    active_ids = set()
    if trace:
        for item in trace:
            trace_map[item.get("agent", "").lower()] = item
            aid = item.get("id")
            status = (item.get("status") or "").lower()
            if aid and status in ("completed", "triggered", "running"):
                active_ids.add(aid)

    for agent in AGENTS:
        titem = trace_map.get(agent["name"].lower()) or {}
        status = (titem.get("status") or "idle").lower()
        if agent["id"] in active_ids and status == "idle":
            status = "completed"
        detail = titem.get("detail") or agent["desc"]
        dot_class = status if status in ("completed", "triggered", "skipped", "running") else "skipped"
        if status == "idle":
            dot_class = "skipped"
        st.markdown(
            f"""
            <div class="tw-agent-row">
                <div class="tw-agent-dot {dot_class}"></div>
                <div style="flex:1">
                    <strong style="font-size:0.88rem">{agent['icon']} {html.escape(agent['name'])}</strong>
                    <span class="tw-badge">{status}</span><br/>
                    <span style="font-size:0.78rem;opacity:0.75">{html.escape(str(detail)[:80])}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def render_agent_grid(active_ids: list | None = None) -> None:
    from agents_registry import AGENTS

    active_ids = set(active_ids or [])
    cols = st.columns(4)
    for i, agent in enumerate(AGENTS):
        cls = "active" if agent["id"] in active_ids else ""
        with cols[i % 4]:
            st.markdown(
                f'<div class="tw-agent-grid-card {cls}">'
                f'<div style="font-size:1.2rem">{agent["icon"]}</div>'
                f'<div style="font-size:0.72rem;font-weight:700">{html.escape(agent["name"][:18])}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


def render_skeleton_loader(count: int = 3) -> None:
    for _ in range(count):
        st.markdown('<div class="tw-skeleton"></div>', unsafe_allow_html=True)


def render_hitl_card(result: dict) -> None:
    """Human-in-the-loop handoff for Person 5."""
    st.markdown(
        f"""
        <div class="tw-escalation">
            <strong>🚨 HITL — Escalation (Person 5)</strong><br/>
            <span style="font-size:0.88rem">
            Case summary for human agent:<br/>
            Intent: {html.escape(str(result.get("intent", "")))} ·
            Confidence: {result.get("confidence", 0):.0%}<br/>
            Booking: {html.escape(str(result.get("booking_summary", {}).get("booking_id", "N/A")))}<br/>
            {html.escape(result.get("escalation_reason", ""))}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_flight_status(flight: dict) -> None:
    status = flight.get("flight_status", "Scheduled")
    delay = flight.get("delay_minutes", 0)
    colors = {"OnTime": "#059669", "Delayed": "#d97706", "Cancelled": "#dc2626", "Scheduled": "#0077b6"}
    labels = {
        "OnTime": "On time",
        "Delayed": f"Delayed {delay // 60}h {delay % 60}m" if delay else "Delayed",
        "Cancelled": "Cancelled by airline",
        "Scheduled": "Scheduled",
    }
    c = colors.get(status, "#64748b")
    label = labels.get(status, status)
    st.markdown(
        f'<span style="background:{c};color:white;padding:0.2rem 0.6rem;border-radius:999px;'
        f'font-size:0.75rem;font-weight:700">{html.escape(label)}</span>',
        unsafe_allow_html=True,
    )


def render_hotel_card(hotel: dict, is_best: bool = False, show_image: bool = True) -> None:
    badge = '<span class="tw-lowest-badge">Best value</span> ' if is_best else ""
    cols = st.columns([1, 2]) if show_image else [1]
    with cols[0] if show_image else st.container():
        if show_image and hotel.get("image_url"):
            try:
                st.image(hotel["image_url"], use_container_width=True)
            except Exception:
                st.caption("Image unavailable")
    with cols[1] if show_image else st.container():
        stars = "★" * hotel.get("stars", 3)
        st.markdown(
            f'<div class="tw-flight-card">{badge}'
            f'<strong>{stars} {html.escape(hotel.get("name", ""))}</strong> '
            f'<span style="float:right;font-weight:800;color:#e85d04">Rs {hotel.get("price_night", 0):,}/night</span><br/>'
            f'<span style="font-size:0.85rem">{html.escape(hotel.get("city", ""))} · '
            f'Rating {hotel.get("rating", 0)}/5 · {hotel.get("reviews_count", 0):,} reviews</span><br/>'
            f'<span style="font-size:0.8rem">{", ".join(hotel.get("amenities", []))}</span><br/>'
            f'<span style="font-size:0.78rem;opacity:0.8">{html.escape(hotel.get("cancellation_policy", ""))}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def render_breadcrumb(parts: list) -> None:
    st.caption(" › ".join(parts))


BOOKING_STEPS = [
    ("search", "Search"),
    ("results", "Results"),
    ("checkout", "Payment & Book"),
    ("done", "Confirmation"),
]


def render_step_bar(state_key: str) -> None:
    current = st.session_state.get(state_key, "search")
    parts = []
    for i, (key, label) in enumerate(BOOKING_STEPS):
        cls = "tw-step-active" if key == current else ("tw-step-done" if _step_index(key) < _step_index(current) else "tw-step-pending")
        parts.append(f'<span class="tw-step {cls}"><span class="tw-step-num">{i + 1}</span>{html.escape(label)}</span>')
    st.markdown(f'<div class="tw-stepper">{"".join(parts)}</div>', unsafe_allow_html=True)


def _step_index(step: str) -> int:
    order = [s[0] for s in BOOKING_STEPS]
    return order.index(step) if step in order else 0


def set_status(message: str, level: str = "info") -> None:
    st.session_state.status_message = {"text": message, "level": level}


def render_status() -> None:
    msg = st.session_state.get("status_message")
    if not msg:
        return
    text = html.escape(msg.get("text", ""))
    level = msg.get("level", "info")
    cls = {"success": "tw-status-success", "warning": "tw-status-warning", "error": "tw-status-error"}.get(level, "tw-status-info")
    st.markdown(f'<div class="tw-status-banner {cls}">{text}</div>', unsafe_allow_html=True)


def render_booking_steps(current: int) -> None:
    steps = ["Search", "Results", "Payment", "Done"]
    st.progress(current / 4, text=f"Step {current}/4: {steps[current - 1] if 1 <= current <= 4 else ''}")


def render_hotel_checkout_gallery(hotel: dict) -> None:
    st.markdown('<div class="tw-hotel-checkout">', unsafe_allow_html=True)
    url = hotel.get("image_url", "")
    if url:
        try:
            st.image(url, use_container_width=True)
        except Exception:
            st.caption("Hero image unavailable")
    images = hotel.get("images") or []
    if len(images) > 1:
        cols = st.columns(min(3, len(images)))
        for col, img in zip(cols, images[:3]):
            with col:
                try:
                    st.image(img, use_container_width=True)
                except Exception:
                    pass
    st.markdown("</div>", unsafe_allow_html=True)


def render_flight_card(flight: dict, is_lowest: bool = False) -> None:
    badge = '<span class="tw-lowest-badge">Lowest Fare</span> ' if is_lowest else ""
    stops = "Non-stop" if flight.get("stops") == 0 else f"{flight.get('stops')} stop"
    st.markdown(
        f'<div class="tw-flight-card tw-animate-in">{badge}'
        f'<strong>{html.escape(flight.get("airline", ""))} {html.escape(flight.get("flight_no", ""))}</strong> '
        f'<span style="float:right;font-weight:800;color:#e85d04">₹{flight.get("price_inr", 0):,}</span><br/>'
        f'<span style="font-size:0.85rem">{flight.get("from")} → {flight.get("to")} · {flight.get("dep")} · {stops} · {flight.get("duration", "")}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_refund_timeline(timeline: list) -> None:
    for step in timeline:
        icon = "✅" if step.get("done") else "⏳"
        st.markdown(f"{icon} **{step.get('step')}** — {step.get('date')}")


def render_ai_response(text: str) -> None:
    with st.container():
        st.markdown('<div class="tw-card"><div class="tw-card-title">💬 AI Response</div>', unsafe_allow_html=True)
        st.markdown(text)
        st.markdown("</div>", unsafe_allow_html=True)
