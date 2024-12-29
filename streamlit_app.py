import streamlit as st
# from global_variables import *
# from db_connection import get_mysql_data
# from ui_components import render_header, render_data, render_sample_elements
# from authentication import authenticate_user

# Page Configuration
st.set_page_config(
    page_title="Restaurant Management App",
    page_icon="🍽️",
    layout="wide",  # Options: "centered", "wide"
    initial_sidebar_state="auto",  # Options: "expanded", "collapsed", "auto"
)

# Custom CSS
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        font-size: 6px;
    }
    .stTitle {
        font-size: 10px;
        color: #2E86C1;
        text-align: center;
    }
    [data-testid="stToolbar"] {
        visibility: hidden;
        height: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Welcome to the Restaurant Management App!")
st.title("Sign In Page")

