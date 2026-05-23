import streamlit as st


def is_logged_in() -> bool:
    return bool(st.session_state.get("logged_in"))


def get_profile() -> dict:
    return st.session_state.get("user_profile", {})


def get_token():
    return st.session_state.get("auth_token")


def get_mobile() -> str:
    profile = get_profile()
    return profile.get("mobile", "")


def login_session(user: dict):
    st.session_state.logged_in = True
    st.session_state.user_profile = user
    st.session_state.user_id = user.get("user_id")


def logout():
    for key in ["logged_in", "user_profile", "user_id", "auth_token"]:
        if key in st.session_state:
            del st.session_state[key]


def restore_session_from_file():
    return False


def is_auth_pending():
    return False


def has_profile():
    return is_logged_in()