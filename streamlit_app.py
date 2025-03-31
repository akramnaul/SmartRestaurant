# Check the streamlit code
# streamlit_app.py
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from database.connect_database import connect_database
from database.execute_stored_procedure import execute_stored_procedure
# from frontend.restaurant_landing_page import user_signin
from database.user_signin import user_signin


def get_ready_page():
  if(user_signin() is True):
    st.write("User Signin Successfully Reached Back @ streamlit_app.py")
    # Check User's Roll / Class ... then ... Redirect to Appropriate Webpage
    if (('Restaurant' in st.session_state) and
        ('RestaurantUser' in st.session_state) and
        ('RestaurantUserPassword' in st.session_state) and
        ('RestaurantUserSigninValid' in st.session_state) and
        (st.session_state['RestaurantUserSigninValid'] is True)):
        st.subheader("Smart Restaurant : Get Ready Page : Successful")
    else:
        st.subheader("Smart Restaurant : Get Ready Page : UnSuccessful")


# JavaScript to Reload the Page
def clear_page():
    st.markdown("""
        <script>
            location.reload();
        </script>
    """, unsafe_allow_html=True)

    st.write("User Signin UnSuccessfully Reached Back @ streamlit_app.py")

st.write("This is some content on the screen.")

if st.button("Clear Screen"):
    clear_page()  # Reloads the page, effectively clearing it


# RestaurantAdmin
# RestaurantCashier
# RestaurantCustomer
# RestaurantOrderTaker
# RestaurantOwner
# RestaurantRider
# RestaurantStation



