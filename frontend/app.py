"""TripWise entry — route to Login or Home."""
import streamlit as st

from layout import apply_theme, init_session
from user_store import is_logged_in

st.set_page_config(page_title="TripWise", page_icon="✈", layout="wide", initial_sidebar_state="expanded")
init_session()
apply_theme()

if is_logged_in():
    st.switch_page("pages/1_Home.py")
else:
    st.switch_page("pages/0_Login.py")
