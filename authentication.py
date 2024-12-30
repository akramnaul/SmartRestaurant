import streamlit as st
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# Function to call the RestaurantSignin stored procedure
def authenticate_user(restaurant, user, password):
    """
    Authenticate a user by calling the RestaurantSignin stored procedure.

    Args:
        restaurant (str): Restaurant name.
        user (str): User name.
        password (str): User password.

    Returns:
        dict: OUT parameters from the stored procedure or error message.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Call the stored procedure with placeholders for OUT parameters
        cursor.callproc('RestaurantSignin', [
            restaurant, user, password,
            '@pRestaurantUserName', '@pStatus', '@pStatusCheck'
        ])

        # Fetch OUT parameters
        cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return {
                'pRestaurantUserName': result[0],
                'pStatus': int(result[1]),
                'pStatusCheck': result[2]
            }
        else:
            return {'error': 'No result from the procedure.'}
    except mysql.connector.Error as err:
        return {'error': f"Database error: {str(err)}"}

# Streamlit UI for authentication
def render_authentication_ui():
    st.subheader("Restaurant Sign-In")

    with st.form("signin_form"):
        restaurant = st.text_input("Restaurant Name", help="Enter your restaurant's name.")
        user = st.text_input("User Name", help="Enter your username.")
        password = st.text_input("Password", type="password", help="Enter your password.")
        submitted = st.form_submit_button("Sign In")

    if submitted:
        if not restaurant or not user or not password:
            st.error("All fields are mandatory.")
            return None

        # Authenticate the user
        response = authenticate_user(restaurant, user, password)

        if 'error' in response:
            st.error(response['error'])
            return None

        if response['pStatus']:
            st.success(f"Welcome, {response['pRestaurantUserName']}!")
            st.info(response['pStatusCheck'])
            return response  # Successful authentication
        else:
            st.warning("Authentication failed.")
            st.info(response['pStatusCheck'])
            return None  # Failed authentication
