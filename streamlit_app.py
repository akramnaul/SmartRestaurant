import streamlit as st
# from global_variables import *
# from db_connection import get_mysql_data
# from ui_components import render_header, render_data, render_sample_elements
# from authentication import authenticate_user

# Main app execution
def main():

    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Select a page:", ["Home", "Sign In"])

    if option == "Home":
        st.title("Welcome to the Restaurant Management App!")
        st.write("Use the sidebar to navigate.")
    elif option == "Sign In":
        st.title("Sign In Page")
        # authentication_main()  # Call the authentication logic from authentication.py
