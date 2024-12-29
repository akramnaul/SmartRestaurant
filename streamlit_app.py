import streamlit as st
# from global_variables import *
# from db_connection import get_mysql_data
# from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
# from ui_components import render_header, render_data, render_sample_elements
# from authentication import authenticate_user

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
        font-size: 12px !important;
    }
    h1 {
        font-family: 'Times New Roman', serif;
        font-size: 24px !important;
        color: #2E86C1 !important;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Titles
st.title("SmartRestaurant !")
st.title("Sign In Page")

st.write("Try signing in here with valid credentials")
