"""Search page hero banners with photography (flights / hotels)."""
import html

import streamlit as st

HERO_IMAGES = {
    "flight": "https://images.unsplash.com/photo-1436491865332-7a61a1099cac?w=1400&q=85",
    "hotel": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1400&q=85",
}

HERO_COPY = {
    "flight": ("Book your flight", "Compare fares · Pick your seat · Pay securely"),
    "hotel": ("Find your stay", "Luxury resorts · Flexible rooms · Best rates"),
}


def render_search_hero(kind: str = "flight") -> None:
    url = HERO_IMAGES.get(kind, HERO_IMAGES["flight"])
    title, sub = HERO_COPY.get(kind, HERO_COPY["flight"])
    st.markdown(
        f'<div class="tw-search-hero tw-search-hero-{html.escape(kind)}">'
        f'<div class="tw-search-hero-bg" style="background-image:url({url})"></div>'
        f'<div class="tw-search-hero-scrim"></div>'
        f'<div class="tw-search-hero-content">'
        f'<span class="tw-search-hero-icon">{"✈" if kind == "flight" else "🏨"}</span>'
        f"<h2>{html.escape(title)}</h2>"
        f"<p>{html.escape(sub)}</p>"
        f"</div></div>",
        unsafe_allow_html=True,
    )
