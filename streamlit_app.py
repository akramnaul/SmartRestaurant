import streamlit as st
# from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, APP_NAME, VERSION, CURRENT_USER, IS_AUTHENTICATED, USER_ROLE, ERROR_MESSAGES, SUCCESS_MESSAGES, GUIDELINES
# from db_connection import get_mysql_data
from authentication import render_authentication_ui
from ui_components import render_header, render_data, render_sample_elements

# Page Configuration
st.set_page_config(
    page_title="SmartRestaurant",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="auto",
)

# Custom CSS
st.markdown(
    """
    <style>
    body {
        font-family: 'Times New Roman', serif;
        font-size: 8px !important;
    }
    h1 {
        font-family: 'Times New Roman', serif;
        font-size: 14px !important;
        color: #2E86C1 !important;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Titles
# st.title("SmartRestaurant : Sign In Page")
# Body
# st.write("Try signing in here with valid credentials")

# Render the header (example of including modular UI components)
render_header()

# Render the authentication UI
# Render the header
st.header("SmartRestaurant - Sign In")

# Render the authentication UI
auth_response = render_authentication_ui()

# If authenticated, proceed to display details
if auth_response:
    st.write("**Authentication Successful!**")
    st.write(f"**User Name:** {auth_response['pRestaurantUserName']}")
    st.write(f"**Status:** {'Success' if auth_response['pStatus'] else 'Failed'}")
    st.write(f"**Status Check Message:** {auth_response['pStatusCheck']}")
