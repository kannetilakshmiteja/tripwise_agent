"""Theme-aware CSS for TripWise Streamlit UI."""

THEME_VARS = {
    "light": {
        "bg": "#fffaf7",
        "surface": "#ffffff",
        "surface2": "#fff3eb",
        "text": "#2d2d2d",
        "muted": "#6b6b6b",
        "primary": "#d04a02",
        "primary2": "#e85d04",
        "accent": "#2d2d2d",
        "accent2": "#464646",
        "nav_bg": "#d04a02",
        "sidebar_bg": "#2d2d2d",
        "nav_strip_bg": "#fff3eb",
        "nav_link": "#2d2d2d",
        "nav_link_muted": "#6b6b6b",
        "nav_text": "#ffffff",
        "success": "#059669",
        "warning": "#d97706",
        "danger": "#dc2626",
        "border": "rgba(45,45,45,0.12)",
        "shadow": "0 4px 20px rgba(0,0,0,0.08)",
        "hero_grad": "linear-gradient(135deg, #464646 0%, #2d2d2d 100%)",
        "card_grad": "linear-gradient(145deg, #ffffff 0%, #fafafa 100%)",
    },
    "dark": {
        "bg": "#0b1220",
        "surface": "#111827",
        "surface2": "#1a2336",
        "text": "#f1f5f9",
        "muted": "#94a3b8",
        "primary": "#d04a02",
        "primary2": "#e85d04",
        "accent": "#2d2d2d",
        "accent2": "#464646",
        "nav_bg": "#d04a02",
        "sidebar_bg": "#1f2937",
        "nav_strip_bg": "#2d3748",
        "nav_link": "#f1f5f9",
        "nav_link_muted": "#cbd5e1",
        "nav_text": "#f1f5f9",
        "success": "#34d399",
        "warning": "#fbbf24",
        "danger": "#f87171",
        "border": "rgba(255,255,255,0.08)",
        "shadow": "0 12px 40px rgba(0,0,0,0.45)",
        "hero_grad": "linear-gradient(135deg, #1f2937 0%, #2d2d2d 100%)",
        "card_grad": "linear-gradient(145deg, #111827 0%, #1e293b 100%)",
    },
}


def get_css(theme: str) -> str:
    t = THEME_VARS.get(theme, THEME_VARS["light"])
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}

#MainMenu, footer, header[data-testid="stHeader"] {{
    visibility: hidden;
    height: 0;
}}

.stApp {{
    background: {t["bg"]};
    color: {t["text"]};
}}
section.main .block-container {{
    background: {t["bg"]};
    border-radius: 16px 0 0 0;
    padding-top: 1.25rem !important;
}}

.block-container {{
    padding-top: 1rem !important;
    max-width: 1400px !important;
}}

.tw-hero {{
    background: {t["hero_grad"]};
    border-radius: 20px;
    padding: 1.5rem 1.75rem;
    color: white;
    box-shadow: {t["shadow"]};
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}}

.tw-hero::after {{
    content: '';
    position: absolute;
    right: -30px;
    top: -30px;
    width: 180px;
    height: 180px;
    background: rgba(255,255,255,0.12);
    border-radius: 50%;
}}

.tw-logo {{
    font-size: 1.75rem;
    font-weight: 800;
    letter-spacing: -0.03em;
}}

.tw-tagline {{
    opacity: 0.92;
    font-size: 0.95rem;
    margin-top: 0.25rem;
}}

.tw-card {{
    background: {t["card_grad"]};
    border: 1px solid {t["border"]};
    border-radius: 16px;
    padding: 1rem 1.1rem;
    box-shadow: {t["shadow"]};
    margin-bottom: 0.75rem;
}}

.tw-card-title {{
    font-weight: 700;
    font-size: 0.9rem;
    color: {t["accent"]};
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}}

.tw-metric {{
    background: {t["surface2"]};
    border-radius: 12px;
    padding: 0.75rem;
    text-align: center;
    border: 1px solid {t["border"]};
}}

.tw-metric-value {{
    font-size: 1.35rem;
    font-weight: 800;
    color: {t["primary"]};
}}

.tw-metric-label {{
    font-size: 0.72rem;
    color: {t["muted"]};
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.tw-chat-user {{
    background: linear-gradient(135deg, {t["accent"]}, {t["accent2"]});
    color: white;
    padding: 0.85rem 1rem;
    border-radius: 16px 16px 4px 16px;
    margin: 0.5rem 0 0.5rem 2rem;
    box-shadow: {t["shadow"]};
    font-size: 0.92rem;
}}

.tw-chat-ai {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    color: {t["text"]};
    padding: 0.85rem 1rem;
    border-radius: 16px 16px 16px 4px;
    margin: 0.5rem 2rem 0.5rem 0;
    box-shadow: {t["shadow"]};
    font-size: 0.92rem;
}}

.tw-escalation {{
    background: linear-gradient(135deg, rgba(220,38,38,0.12), rgba(217,119,6,0.12));
    border: 1px solid {t["danger"]};
    border-radius: 14px;
    padding: 1rem;
    margin: 0.75rem 0;
}}

.tw-agent-row {{
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.55rem 0;
    border-bottom: 1px solid {t["border"]};
}}

.tw-agent-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}}

.tw-agent-dot.completed {{ background: {t["success"]}; box-shadow: 0 0 8px {t["success"]}; }}
.tw-agent-dot.triggered {{ background: {t["danger"]}; box-shadow: 0 0 8px {t["danger"]}; }}
.tw-agent-dot.skipped {{ background: {t["muted"]}; }}
.tw-agent-dot.running {{ background: {t["warning"]}; animation: pulse 1s infinite; }}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.4; }}
}}

.tw-rec-item {{
    background: {t["surface2"]};
    border-left: 4px solid {t["primary"]};
    padding: 0.65rem 0.85rem;
    border-radius: 0 10px 10px 0;
    margin-bottom: 0.5rem;
}}

.tw-badge {{
    display: inline-block;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    background: {t["surface2"]};
    color: {t["accent"]};
    border: 1px solid {t["border"]};
    margin-right: 0.35rem;
}}

.tw-confidence-high {{ color: {t["success"]}; font-weight: 700; }}
.tw-confidence-mid {{ color: {t["warning"]}; font-weight: 700; }}
.tw-confidence-low {{ color: {t["danger"]}; font-weight: 700; }}

/* Streamlit widget overrides */
div[data-testid="stSidebar"] {{
    background: {t["surface"]} !important;
    border-right: 1px solid {t["border"]};
}}

.stTextInput input, .stTextArea textarea {{
    background: {t["surface"]} !important;
    color: {t["text"]} !important;
    border: 1px solid {t["border"]} !important;
    border-radius: 12px !important;
}}

.stButton > button {{
    background: linear-gradient(135deg, {t["primary"]}, {t["primary2"]}) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 0.55rem 1.25rem !important;
    width: 100%;
}}

.stButton > button:hover {{
    filter: brightness(1.08);
    transform: translateY(-1px);
}}

/* Mobile responsive */
@media (max-width: 768px) {{
    .block-container {{
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }}
    .tw-hero {{
        padding: 1rem;
        border-radius: 14px;
    }}
    .tw-logo {{
        font-size: 1.35rem;
    }}
    .tw-chat-user {{
        margin-left: 0.5rem;
    }}
    .tw-chat-ai {{
        margin-right: 0.5rem;
    }}
    .tw-metric-value {{
        font-size: 1.1rem;
    }}
}}

@media (max-width: 480px) {{
    .tw-hero {{
        padding: 0.85rem;
    }}
    .tw-card {{
        padding: 0.75rem;
    }}
}}

.tw-logo-nav {{
    font-size: 1.35rem;
    font-weight: 800;
    color: {t["primary"]};
}}

.tw-form-section {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 16px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    box-shadow: {t["shadow"]};
}}

.tw-form-title {{
    font-weight: 700;
    color: {t["accent"]};
    margin-bottom: 0.75rem;
    font-size: 0.95rem;
}}

.tw-flight-card {{
    border-left: 4px solid {t["primary"]} !important;
    background: {t["card_grad"]};
    border: 1px solid {t["border"]};
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 0.65rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.tw-flight-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.12);
}}

.tw-lowest-badge {{
    background: linear-gradient(135deg, {t["success"]}, #10b981);
    color: white;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 700;
    animation: pulse 2s infinite;
}}

.tw-agent-grid-card {{
    background: {t["surface2"]};
    border: 1px solid {t["border"]};
    border-radius: 12px;
    padding: 0.65rem;
    text-align: center;
    min-height: 90px;
}}

.tw-agent-grid-card.active {{
    border-color: {t["primary"]};
    box-shadow: 0 0 12px rgba(232,93,4,0.35);
}}

.tw-offer-card {{
    background: linear-gradient(135deg, {t["accent"]}, {t["accent2"]});
    color: white;
    border-radius: 12px;
    padding: 0.85rem;
    min-width: 160px;
    display: inline-block;
    margin-right: 0.5rem;
}}

.tw-skeleton {{
    background: linear-gradient(90deg, {t["surface2"]} 25%, {t["surface"]} 50%, {t["surface2"]} 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 8px;
    height: 48px;
    margin-bottom: 0.5rem;
}}

.tw-checkout-panel {{
    background: linear-gradient(145deg, {t["surface"]}, {t["surface2"]});
    border: 2px solid {t["primary"]};
    border-radius: 18px;
    padding: 1.35rem;
    margin: 1rem 0;
    box-shadow: 0 8px 32px rgba(232, 93, 4, 0.15);
}}

.tw-api-live {{
    color: {t["success"]};
    font-weight: 700;
    font-size: 0.8rem;
}}

.tw-api-demo {{
    color: {t["warning"]};
    font-weight: 700;
    font-size: 0.8rem;
}}

.tw-navbar {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}}

.tw-nav-logo {{
    height: 32px;
    vertical-align: middle;
}}

.tw-stepper {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 1rem 0;
    padding: 0.75rem;
    background: {t["surface"]};
    border-radius: 14px;
    border: 1px solid {t["border"]};
}}

.tw-step {{
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.4rem 0.75rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
}}

.tw-step-num {{
    width: 1.25rem;
    height: 1.25rem;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
}}

.tw-step-active {{
    background: linear-gradient(135deg, {t["primary"]}, {t["primary2"]});
    color: white;
}}

.tw-step-active .tw-step-num {{
    background: rgba(255,255,255,0.3);
}}

.tw-step-done {{
    background: {t["surface2"]};
    color: {t["success"]};
    border: 1px solid {t["success"]};
}}

.tw-step-pending {{
    background: {t["surface2"]};
    color: {t["muted"]};
}}

.tw-status-banner {{
    padding: 0.75rem 1rem;
    border-radius: 12px;
    margin: 0.5rem 0 1rem;
    font-weight: 600;
    font-size: 0.9rem;
}}

.tw-status-success {{
    background: rgba(5, 150, 105, 0.12);
    border: 1px solid {t["success"]};
    color: {t["success"]};
}}

.tw-status-warning {{
    background: rgba(217, 119, 6, 0.12);
    border: 1px solid {t["warning"]};
    color: {t["warning"]};
}}

.tw-status-error {{
    background: rgba(220, 38, 38, 0.12);
    border: 1px solid {t["danger"]};
    color: {t["danger"]};
}}

.tw-status-info {{
    background: rgba(0, 119, 182, 0.1);
    border: 1px solid {t["accent"]};
    color: {t["accent"]};
}}

.tw-agent-card {{
    background: {t["card_grad"]};
    border: 1px solid {t["border"]};
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    min-height: 140px;
}}

.tw-promo-card {{
    background: {t["card_grad"]};
    border: 2px solid transparent;
    border-image: linear-gradient(135deg, {t["accent"]}, {t["primary"]}) 1;
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 0.5rem;
}}

.tw-pipeline {{
    background: {t["surface2"]};
    border-radius: 12px;
    padding: 0.85rem 1rem;
    margin: 0.75rem 0 1.25rem;
    font-size: 0.85rem;
    text-align: center;
}}

.tw-pipe-node {{
    display: inline-block;
    padding: 0.25rem 0.6rem;
    background: {t["accent"]};
    color: white;
    border-radius: 8px;
    font-weight: 600;
    margin: 0 0.15rem;
}}

.tw-pipe-esc {{
    background: {t["danger"]};
}}

.tw-hotel-checkout {{
    border-radius: 16px;
    overflow: hidden;
    box-shadow: {t["shadow"]};
    margin-bottom: 1rem;
}}

.tw-hotel-checkout img {{
    border-radius: 12px;
}}

.tw-success-check {{
    color: {t["success"]};
    font-weight: 800;
    font-size: 1.1rem;
    padding: 0.5rem 0;
}}

div[data-testid="stSidebar"] [data-testid="stSidebarNav"] {{
    font-size: 0.85rem;
}}

.stButton > button[kind="primary"] {{
    min-height: 2.75rem !important;
}}

/* Sidebar — warm charcoal */
section[data-testid="stSidebar"],
div[data-testid="stSidebar"],
[data-testid="stSidebar"] {{
    background: {t.get("sidebar_bg", t["accent"])} !important;
    background-color: {t.get("sidebar_bg", t["accent"])} !important;
    border-right: 3px solid {t["primary"]} !important;
}}
section[data-testid="stSidebar"] > div,
div[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"] {{
    background: transparent !important;
    background-color: transparent !important;
}}
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {{
    color: #f1f5f9 !important;
}}
section[data-testid="stSidebar"] hr {{
    border-color: rgba(255,255,255,0.2) !important;
}}
div[data-testid="stSidebarNav"] {{
    padding-top: 0.5rem !important;
}}
div[data-testid="stSidebarNav"] span,
div[data-testid="stSidebarNav"] p,
div[data-testid="stSidebarNav"] a {{
    color: #f1f5f9 !important;
}}
div[data-testid="stSidebarNav"] a {{
    border-radius: 10px !important;
    margin: 3px 0 !important;
    padding: 0.5rem 0.75rem !important;
    color: #ffffff !important;
    background: rgba(255,255,255,0.08) !important;
}}
div[data-testid="stSidebarNav"] a:hover {{
    background: rgba(255,255,255,0.14) !important;
}}
div[data-testid="stSidebarNav"] a[aria-current="page"] {{
    background: {t["primary"]} !important;
    color: white !important;
    font-weight: 700 !important;
    border-left: 3px solid #ffffff !important;
    box-shadow: none !important;
}}
.tw-sidebar-brand .tw-sidebar-logo-text {{
    color: white !important;
    -webkit-text-fill-color: white !important;
    background: none !important;
}}
.tw-sidebar-brand .tw-sidebar-tagline {{
    color: #bae6fd !important;
}}
.tw-sidebar-user {{
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: white !important;
}}
.tw-sidebar-hint {{
    color: #94a3b8 !important;
}}
.tw-sidebar-brand {{
    padding: 0.75rem 0.5rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.25);
    margin-bottom: 0.75rem;
    background: rgba(0,0,0,0.15);
    border-radius: 12px;
}}
.tw-sidebar-pill {{
    display: inline-block;
    margin-top: 0.35rem;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.72rem;
    background: rgba(255,255,255,0.2) !important;
    color: white !important;
}}

/* Top navbar — orange brand bar + clean nav strip */
.tw-topnav-wrap {{
    background: {t["nav_bg"]} !important;
    border: none;
    border-radius: 10px 10px 0 0;
    padding: 0.7rem 1.2rem;
    margin-bottom: 0;
    box-shadow: 0 4px 14px rgba(208,74,2,0.25);
}}
.tw-topnav-wrap .tw-logo-nav {{
    color: {t["nav_text"]} !important;
    font-weight: 800;
}}
.tw-topnav-wrap .tw-topnav-pill {{
    background: rgba(255,255,255,0.22) !important;
    color: {t["nav_text"]} !important;
    font-weight: 600;
    font-size: 0.75rem;
}}
.tw-nav-strip {{
    background: {t.get("nav_strip_bg", t["surface2"])} !important;
    border: 1px solid rgba(208,74,2,0.2);
    border-top: none;
    border-radius: 0 0 12px 12px;
    padding: 0.6rem 0.85rem 0.7rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 4px 16px rgba(208,74,2,0.08);
}}
.tw-nav-strip div[data-testid="stPageLink"] a {{
    color: {t.get("nav_link", t["text"])} !important;
    border-radius: 8px !important;
    padding: 0.4rem 0.7rem !important;
    font-weight: 600 !important;
}}
.tw-nav-strip div[data-testid="stPageLink"] a[aria-current="page"] {{
    background: {t["primary"]} !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}}
.tw-nav-strip div[data-testid="stPageLink"] a:hover {{
    background: rgba(208,74,2,0.22) !important;
    color: {t["primary"]} !important;
}}
/* Dark mode: nav strip readable on charcoal */
section.main:has(.tw-app-theme-dark) .tw-nav-strip {{
    background: {t.get("nav_strip_bg", "#2d3748")} !important;
    border-color: rgba(255,255,255,0.15) !important;
}}
section.main:has(.tw-app-theme-dark) .tw-nav-strip div[data-testid="stPageLink"] a {{
    color: #f1f5f9 !important;
}}
section.main:has(.tw-app-theme-dark) .tw-nav-strip div[data-testid="stPageLink"] a[aria-current="page"] {{
    color: #ffffff !important;
}}
section.main:has(.tw-app-theme-dark) .tw-nav-strip .stButton > button {{
    background: rgba(255,255,255,0.1) !important;
    color: #f1f5f9 !important;
    border-color: rgba(255,255,255,0.25) !important;
}}
section.main:has(.tw-app-theme-dark) .tw-nav-strip .stButton > button:hover {{
    background: {t["primary"]} !important;
    color: #ffffff !important;
}}
.tw-app-theme {{
    display: none;
}}
.tw-nav-strip .stButton > button {{
    white-space: nowrap !important;
    min-width: 5.5rem !important;
    font-size: 0.8rem !important;
    padding: 0.45rem 0.65rem !important;
    line-height: 1.2 !important;
    background: white !important;
    color: {t["primary"]} !important;
    border: 1px solid rgba(208,74,2,0.35) !important;
}}
.tw-nav-strip .stButton > button:hover {{
    background: {t["primary"]} !important;
    color: white !important;
}}
div[data-testid="stPageLink"] a {{
    white-space: nowrap !important;
    font-weight: 600 !important;
}}
.tw-nav-spacer {{
    display: block;
    min-height: 1px;
}}
.tw-topnav {{
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.tw-topnav-left {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}
.tw-topnav-pill {{
    font-size: 0.72rem;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    background: {t["surface2"]};
}}

/* Hero cinema (home) */
.tw-hero-cinema {{
    position: relative;
    min-height: 360px;
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 1.5rem;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    animation: heroZoom 18s ease-in-out infinite alternate;
    border: 2px solid rgba(255,255,255,0.25);
    box-shadow: 0 16px 48px rgba(0,60,120,0.25);
}}
.tw-hero-plane {{
    position: absolute;
    top: 22%;
    font-size: 2.5rem;
    z-index: 2;
    animation: flyAcross 14s linear infinite;
    filter: drop-shadow(0 6px 12px rgba(0,0,0,0.4));
}}
.tw-hero-cloud {{
    position: absolute;
    font-size: 2rem;
    opacity: 0.5;
    animation: cloudDrift 20s linear infinite;
}}
.tw-hero-cinema-overlay {{
    position: relative;
    z-index: 1;
    padding: 2.5rem 2rem 2rem;
    background: linear-gradient(105deg, rgba(0,40,80,0.85) 0%, rgba(0,119,182,0.55) 45%, rgba(232,93,4,0.35) 100%);
    min-height: 320px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}}
.tw-brand-mega {{
    font-size: 3.25rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: white;
    text-shadow: 0 4px 24px rgba(0,0,0,0.35);
    line-height: 1.1;
    margin: 0;
}}
.tw-hero-cinema .tw-tagline {{
    color: rgba(255,255,255,0.92);
    font-size: 1.05rem;
    margin-top: 0.5rem;
}}
.tw-glass-card {{
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 16px;
    padding: 1.25rem;
    margin-top: 1.25rem;
}}

/* Login */
.tw-login-split {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    align-items: stretch;
    margin-top: 1rem;
}}
@media (max-width: 900px) {{
    .tw-login-split {{ grid-template-columns: 1fr; }}
}}
/* Login — true side-by-side via column markers */
section.main:has(.tw-login-page-marker) .block-container {{
    max-width: 100% !important;
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
    background: {t["bg"]} !important;
}}
section.main:has(.tw-login-page-marker) [data-testid="stHorizontalBlock"] {{
    align-items: flex-start !important;
    gap: 1rem !important;
}}
section.main:has(.tw-login-page-marker) [data-testid="column"] {{
    padding: 0 !important;
    min-width: 0 !important;
}}
section.main:has(.tw-login-page-marker) iframe {{
    border-radius: 18px !important;
    width: 100% !important;
}}
section.main:has(.tw-login-page-marker) [data-testid="stVerticalBlockBorderWrapper"] {{
    height: 700px !important;
    max-height: calc(100vh - 4rem) !important;
}}
.tw-login-visual-full {{
    position: relative;
    width: 100%;
    min-height: calc(100vh - 5.5rem);
    height: 100%;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 16px 48px rgba(0,0,0,0.25);
    background-size: cover !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    animation: loginFloat 14s ease-in-out infinite;
}}
.tw-login-visual-panel {{
    position: relative;
    min-height: calc(100vh - 5.5rem);
    width: 100%;
    border-radius: 20px;
    overflow: hidden;
    background-size: cover !important;
    background-position: center center !important;
}}
.tw-login-cloud {{
    position: absolute;
    font-size: 2.5rem;
    opacity: 0.45;
    z-index: 2;
    animation: cloudDrift 22s linear infinite;
}}
.tw-login-cloud-1 {{ top: 8%; left: 8%; }}
.tw-login-cloud-2 {{ top: 14%; right: 12%; animation-delay: 6s; }}
.tw-login-step-badge {{
    position: absolute;
    top: 1.25rem;
    left: 1.25rem;
    z-index: 6;
    background: rgba(208,74,2,0.92);
    color: white;
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
}}
.tw-plane-colored {{
    display: inline-block;
    font-size: 7.5rem;
    line-height: 1;
    background: linear-gradient(145deg, #ffe8cc 0%, #ffb347 25%, #d04a02 70%, #ff6b35 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 10px 28px rgba(208,74,2,0.65));
}}
.tw-hero-plane.tw-plane-colored {{
    font-size: 3rem;
    top: 18%;
}}
.tw-login-scrim-side {{
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba(45,45,45,0.55) 0%, rgba(208,74,2,0.2) 100%);
    pointer-events: none;
}}
.tw-login-plane-rise {{
    position: absolute;
    top: 12%;
    right: 6%;
    z-index: 5;
    animation: planeRise 7s ease-in-out infinite;
}}
.tw-login-plane-rise .tw-plane-colored {{
    font-size: 7.5rem;
}}
.tw-login-plane-trail {{
    position: absolute;
    top: 26%;
    right: 14%;
    width: 6px;
    height: 160px;
    background: linear-gradient(180deg, rgba(255,200,120,0.85), transparent);
    z-index: 4;
    animation: trailRise 7s ease-in-out infinite;
    border-radius: 4px;
}}
.tw-login-hero-text {{
    position: absolute;
    bottom: 2rem;
    left: 1.75rem;
    right: 1rem;
    z-index: 5;
    color: white;
    text-shadow: 0 2px 16px rgba(0,0,0,0.55);
    pointer-events: none;
}}
.tw-login-hero-text .tw-brand-mega {{
    font-size: 2.75rem;
    font-weight: 800;
    margin: 0;
}}
.tw-login-tagline {{
    margin: 0.4rem 0 0;
    font-size: 1.05rem;
    opacity: 0.95;
}}
.tw-login-sub {{
    font-size: 0.9rem;
    margin-top: 0.5rem;
    opacity: 0.88;
}}
.tw-login-form-panel-marker {{
    display: none;
}}
section.main:has(.tw-login-page-marker) .stTextInput input,
section.main:has(.tw-login-page-marker) .stSelectbox input {{
    border-radius: 10px !important;
}}

/* Search hero — flight / hotel photography */
.tw-search-hero {{
    position: relative;
    min-height: 200px;
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 1.25rem;
    box-shadow: {t["shadow"]};
}}
.tw-search-hero-bg {{
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center;
    animation: loginFloat 16s ease-in-out infinite;
}}
.tw-search-hero-scrim {{
    position: absolute;
    inset: 0;
    background: linear-gradient(105deg, rgba(45,45,45,0.75) 0%, rgba(208,74,2,0.45) 100%);
}}
.tw-search-hero-content {{
    position: relative;
    z-index: 2;
    padding: 2rem 2rem 1.75rem;
    color: white;
}}
.tw-search-hero-icon {{
    font-size: 2.5rem;
    display: block;
    margin-bottom: 0.35rem;
}}
.tw-search-hero-content h2 {{
    margin: 0;
    font-size: 1.75rem;
    font-weight: 800;
}}
.tw-search-hero-content p {{
    margin: 0.4rem 0 0;
    opacity: 0.92;
    font-size: 1rem;
}}

/* Checkout side-by-side panels */
.tw-checkout-split-label {{
    font-weight: 700;
    color: {t["primary"]};
    font-size: 0.95rem;
    margin-bottom: 0.65rem;
    padding-bottom: 0.35rem;
    border-bottom: 2px solid {t["surface2"]};
}}
section.main [data-testid="stHorizontalBlock"]:has(.tw-checkout-split-label) {{
    align-items: flex-start !important;
}}
/* Flight checkout — MakeMyTrip-style layout */
.tw-checkout-page {{
    max-width: 1280px;
    margin: 0 auto 1.5rem;
}}
.tw-flight-checkout-banner {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    background: linear-gradient(135deg, {t["primary"]} 0%, #ff8c42 100%);
    color: white;
    padding: 1.1rem 1.35rem;
    border-radius: 14px;
    margin-bottom: 1rem;
    box-shadow: 0 8px 24px rgba(208,74,2,0.28);
}}
.tw-flight-checkout-route {{
    display: flex;
    align-items: center;
    gap: 0.85rem;
}}
.tw-flight-checkout-icon {{
    font-size: 2.25rem;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
}}
.tw-flight-checkout-meta {{
    font-size: 0.88rem;
    opacity: 0.92;
    margin-top: 0.2rem;
}}
.tw-flight-checkout-fare {{
    font-size: 1rem;
    text-align: right;
}}
.tw-flight-checkout-fare strong {{
    font-size: 1.35rem;
}}
section.main:has(.tw-checkout-page) [data-testid="stHorizontalBlock"] {{
    align-items: flex-start !important;
    gap: 1.25rem !important;
}}
section.main:has(.tw-checkout-page) [data-testid="column"]:nth-child(2) {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 16px;
    padding: 1rem 1.1rem !important;
    box-shadow: {t["shadow"]};
}}
.tw-checkout-pay-sticky {{
    border-left: 3px solid {t["primary"]};
    padding-left: 0.75rem;
}}
body.tw-theme-dark .stApp,
section.main:has(.tw-app-theme-dark) .block-container {{
    background: {t["bg"]} !important;
    color: {t["text"]};
}}
body.tw-theme-light .stApp {{
    background: {t["bg"]} !important;
}}
.tw-login-card {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 20px;
    padding: 1.75rem;
    box-shadow: {t["shadow"]};
}}
.tw-login-brand {{
    font-size: 2rem;
    font-weight: 800;
    color: {t["primary"]};
    margin-bottom: 0.25rem;
}}

/* Agents list rows */
.tw-agent-row {{
    display: grid;
    grid-template-columns: 48px 1fr auto;
    gap: 1rem;
    align-items: center;
    background: {t["card_grad"]};
    border: 1px solid {t["border"]};
    border-radius: 12px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.5rem;
    border-left: 4px solid {t["accent"]};
}}
.tw-agent-row-icon {{
    font-size: 1.5rem;
    text-align: center;
}}
.tw-agent-row-body strong {{
    font-size: 0.95rem;
}}
.tw-agent-row-body span {{
    font-size: 0.8rem;
    opacity: 0.8;
    display: block;
}}
.tw-agents-header {{
    margin-bottom: 1rem;
}}

/* Traveller / hotel prefs / seat map */
.tw-traveller-panel,
.tw-hotel-prefs-panel {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 16px;
    padding: 1rem 1.15rem;
    margin-bottom: 1rem;
    box-shadow: {t["shadow"]};
    border-left: 4px solid {t["primary"]};
}}
.tw-seat-map {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 16px;
    padding: 1rem;
    margin-bottom: 1rem;
    overflow-x: auto;
    box-shadow: {t["shadow"]};
}}
.tw-seat-legend {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.5rem 0 0.75rem;
}}
.tw-seat-chip {{
    font-size: 0.72rem;
    padding: 0.25rem 0.55rem;
    border-radius: 999px;
    font-weight: 600;
}}
.tw-seat-window {{ background: #dbeafe; color: #1e40af; }}
.tw-seat-aisle {{ background: #ffedd5; color: #9a3412; }}
.tw-seat-extra {{ background: #fef3c7; color: #92400e; }}
.tw-seat-booked {{ background: #fee2e2; color: #991b1b; }}
.tw-hotel-price-total {{
    font-size: 1.15rem;
    font-weight: 800;
    color: {t["primary"]};
    margin: 0.5rem 0 0;
}}
.tw-seat-occupied {{
    background: #d1d5db !important;
    color: #6b7280 !important;
    border: 1px solid #9ca3af;
    cursor: not-allowed;
}}
.tw-seat-fuselage {{
    background: {t["surface2"]};
    border-radius: 14px;
    padding: 0.75rem;
    border: 1px dashed {t["border"]};
}}
.tw-seat-nose {{
    text-align: center;
    font-weight: 700;
    color: {t["primary"]};
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
}}
.tw-seat-cell {{
    text-align: center;
    padding: 0.35rem;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 600;
}}
.tw-checkout-substeps {{
    display: flex;
    gap: 0.5rem;
    margin: 0.5rem 0 1rem;
}}
.tw-checkout-sub {{
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
}}
.tw-checkout-sub-active {{
    background: {t["primary"]};
    color: white;
}}
.tw-checkout-sub-pending {{
    background: {t["surface2"]};
    color: {t["muted"]};
}}
.stButton > button:hover {{
    transform: translateY(-1px);
}}
.stButton > button[kind="primary"] {{
    background: {t["primary"]} !important;
    border-color: {t["primary"]} !important;
    color: white !important;
}}
.stButton > button[kind="primary"]:hover {{
    background: {t["primary2"]} !important;
    border-color: {t["primary2"]} !important;
}}
.stButton > button:disabled {{
    background: #e5e7eb !important;
    color: #9ca3af !important;
    border-color: #d1d5db !important;
}}
.tw-login-caption {{
    font-size: 0.95rem;
    color: {t["muted"]};
    margin-top: 0.5rem;
}}
.tw-login-form-inner {{
    min-height: calc(100vh - 8rem);
    display: flex;
    flex-direction: column;
}}
.tw-seat-grid-head {{
    display: grid;
    grid-template-columns: 0.55fr 1fr 1fr 1fr 0.25fr 1fr 1fr 1fr;
    gap: 0.35rem;
    text-align: center;
    font-weight: 700;
    font-size: 0.8rem;
    color: {t["primary"]};
    margin-bottom: 0.5rem;
}}
.tw-seat-aisle {{
    color: {t["muted"]};
    font-size: 0.7rem;
}}
.tw-seat-map .stButton > button {{
    min-height: 2.6rem !important;
    font-size: 0.72rem !important;
    padding: 0.25rem 0.15rem !important;
    line-height: 1.15 !important;
}}
.tw-seat-map .stButton > button[kind="primary"] {{
    background: {t["primary"]} !important;
    color: white !important;
}}
section.main:has(.tw-app-theme-dark) .stApp,
section.main:has(.tw-app-theme-dark) .block-container {{
    background: {t["bg"]} !important;
    color: {t["text"]} !important;
}}
section.main:has(.tw-app-theme-dark) .tw-nav-strip {{
    background: #2d3748 !important;
    border-color: rgba(255,255,255,0.12) !important;
}}
section.main:has(.tw-app-theme-dark) .tw-nav-strip div[data-testid="stPageLink"] a {{
    color: #e2e8f0 !important;
}}
section.main:has(.tw-app-theme-dark) .tw-topnav-wrap {{
    background: {t["primary"]} !important;
}}
section.main:has(.tw-app-theme-dark) [data-testid="stSidebar"] {{
    background: #1e293b !important;
}}
</style>
"""


def get_animations(theme: str) -> str:
    return """
<style>
@keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
.tw-animate-in { animation: fadeUp 0.5s ease forwards; }
.stButton > button { transition: all 0.2s ease !important; }
.stButton > button:active { transform: scale(0.98) !important; }
</style>
"""
