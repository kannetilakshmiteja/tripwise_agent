import streamlit as st
import api_client

from layout import apply_theme, init_session
from user_store import is_logged_in, login_session

st.set_page_config(
    page_title="Login | TripWise",
    page_icon="✈",
    layout="wide"
)

init_session()
apply_theme()

if is_logged_in():
    st.switch_page("pages/1_Home.py")

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "register"


st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #3b8f7f, #1e73be);
}

.auth-title {
    text-align: center;
    color: white;
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 20px;
}

.auth-container {
    max-width: 1100px;
    margin: auto;
    background: white;
    display: flex;
    min-height: 650px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
}

.left-panel {
    flex: 1;
    background-image: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.25)),
    url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
    background-size: cover;
    background-position: center;
    padding: 80px 60px;
    color: white;
}

.left-panel h2 {
    font-size: 28px;
    margin-top: 40px;
}

.left-panel p {
    font-size: 20px;
}

.glass-card {
    margin-top: 300px;
    padding: 25px;
    border-radius: 18px;
    background: rgba(0,0,0,0.35);
    backdrop-filter: blur(8px);
}

.right-panel {
    flex: 1;
    padding: 70px 80px;
}

.logo {
    text-align: center;
    font-size: 45px;
    color: #1e88e5;
}

.form-title {
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    color: black;
    margin-bottom: 30px;
}

.switch-text {
    text-align: center;
    color: #666;
    margin-top: 20px;
}

.stButton > button {
    border-radius: 12px;
    height: 45px;
    font-weight: 700;
}

div[data-testid="stTextInput"] input {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="auth-title">#DailyUI #001</div>', unsafe_allow_html=True)

left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("""
    <div class="left-panel">
        <h2>Welcome Adventurer! The World Awaits.</h2>
        <p>Embark On Your Next Journey</p>

        <div class="glass-card">
            <h2>Wander, Explore,<br>Experience</h2>
            <p>Unlock New Destinations, Exclusive Deals,<br>
            And Travel Inspiration Tailored Just For You.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown('<div class="right-panel">', unsafe_allow_html=True)
    st.markdown('<div class="logo">✈️</div>', unsafe_allow_html=True)

    if st.session_state.auth_mode == "register":
        st.markdown('<div class="form-title">Create Your Free Account</div>', unsafe_allow_html=True)

        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        mobile = st.text_input("Mobile Number")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        agree = st.checkbox("I agree to the Terms and Conditions and Privacy Policy", value=True)

        if st.button("Create Your Account", type="primary", use_container_width=True):
            if not full_name or not email or not mobile or not password:
                st.error("All fields are required")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif not agree:
                st.error("Please accept Terms and Conditions")
            else:
                result = api_client.register_user(
                    full_name,
                    email,
                    mobile,
                    password
                )

                if result.get("success"):
                    st.success("Registration successful. Please login now.")
                    st.session_state.auth_mode = "login"
                    st.rerun()
                else:
                    st.error(result.get("error", "Registration failed"))

        st.markdown('<div class="switch-text">Already Have An Account?</div>', unsafe_allow_html=True)

        if st.button("Log In", use_container_width=True):
            st.session_state.auth_mode = "login"
            st.rerun()

    else:
        st.markdown('<div class="form-title">Welcome Back</div>', unsafe_allow_html=True)

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Log In", type="primary", use_container_width=True):
            result = api_client.login_user(email, password)

            if result.get("success"):
                login_session(result["user"])
                st.success("Login successful")
                st.switch_page("pages/1_Home.py")
            else:
                st.error(result.get("error", "Login failed"))

        st.markdown('<div class="switch-text">New User?</div>', unsafe_allow_html=True)

        if st.button("Create Your Account", use_container_width=True):
            st.session_state.auth_mode = "register"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)