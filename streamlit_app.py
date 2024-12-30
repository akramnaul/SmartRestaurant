import streamlit as st
# from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
# , APP_NAME, VERSION, CURRENT_USER, IS_AUTHENTICATED, USER_ROLE, ERROR_MESSAGES, SUCCESS_MESSAGES, GUIDELINES
# from global_variables import *
# from db_connection import get_mysql_data
# from authentication import render_authentication_ui
# from ui_components import render_header, render_data, render_sample_elements
# from authentication import authenticate_user

# Titles
# st.title("SmartRestaurant : Sign In Page")
# Body
# st.write("Try signing in here with valid credentials")

st.title("SmartRestaurant : Sign In Page")

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
