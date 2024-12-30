import streamlit as st
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from global_variables import *
from db_connection import get_mysql_data
from authentication import render_authentication_ui
from ui_components import render_header, render_data, render_sample_elements
from authentication import authenticate_user

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
st.title("SmartRestaurant : Sign In Page")
# Body
st.write("Try signing in here with valid credentials")

def main():
    st.title("WebApp for Restaurant Management")

    # Render the header (example of including modular UI components)
    render_header()

    # Render the authentication UI
    auth_response = render_authentication_ui()

    # If authenticated, proceed with the application
    if auth_response:
        st.write("Proceeding with the application...")
        # Add more UI components or logic here
        render_data()  # Example of rendering some data
        render_sample_elements()  # Example of rendering other UI elements

if __name__ == "__main__":
    main()

