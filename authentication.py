import streamlit as st
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# In authentication.py

def authenticate_user(restaurant, user, password):
    try:
        # Your logic for MySQL connection and procedure call...
        
        result = fetch_result_from_mysql()  # Example function

        if result:
            return {
                'pRestaurantUserName': result[0],
                'pStatus': result[1],
                'pStatusCheck': result[2]
            }
        else:
            return {'error': 'Authentication failed. No result returned.'}

    except Exception as e:
        return {'error': f"An error occurred: {str(e)}"}






def render_authentication_ui():
    """
    Streamlit UI for authentication.
    """
    st.subheader("Restaurant Signin")

    with st.form("signin_form"):
        restaurant = st.text_input("Restaurant Name")
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In")

    if submitted:
        if not restaurant or not user or not password:
            st.error("All fields are required!")
            return

    response = authenticate_user(restaurant, user, password)

if 'error' in response:
    st.error(response['error'])
else:
    if response.get('pStatus') == 1:
        st.success(f"Welcome, {response['pRestaurantUserName']}!")
        st.info(response['pStatusCheck'])
    else:
        st.warning("Authentication failed.")
        st.info(response['pStatusCheck'])

if __name__ == "__main__":
    render_authentication_ui()
