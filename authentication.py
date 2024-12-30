import streamlit as st
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def authenticate_user(restaurant, user, password):
    """
    Authenticate a user by calling the RestaurantSignin stored procedure.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Initialize OUT parameters
        cursor.execute("SET @pRestaurantUserName = NULL;")
        cursor.execute("SET @pStatus = NULL;")
        cursor.execute("SET @pStatusCheck = NULL;")

        # Call the stored procedure
        cursor.callproc('RestaurantSignin', [
            restaurant, user, password,
            '@pRestaurantUserName', '@pStatus', '@pStatusCheck'
        ])

        # Retrieve OUT parameters in the same session
        cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
        out_params = cursor.fetchone()

        # Debugging
        print(f"DEBUG: OUT Parameters fetched: {out_params}")

        if out_params:
            return {
                'pRestaurantUserName': out_params[0],
                'pStatus': bool(out_params[1]),
                'pStatusCheck': out_params[2]
            }
        else:
            return {
                'error': 'Stored procedure executed but returned no data.'
            }

    except mysql.connector.Error as err:
        print(f"DEBUG: MySQL error: {str(err)}")
        return {'error': f"MySQL error: {str(err)}'}
    except Exception as e:
        print(f"DEBUG: Unexpected error: {str(e)}")
        return {'error': f"Unexpected error: {str(e)}'}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def render_authentication_ui():
    st.subheader("Restaurant Signin")

    with st.form("signin_form"):
        restaurant = st.text_input("Restaurant Name", help="Enter your restaurant's name.")
        user = st.text_input("User Name", help="Enter your username.")
        password = st.text_input("Password", type="password", help="Enter your password.")
        submitted = st.form_submit_button("Signin")

    if submitted:
        if not restaurant or not user or not password:
            st.error("All fields are mandatory.")
            return None

        # Authenticate the user
        response = authenticate_user(restaurant, user, password)

        if 'error' in response:
            st.error(response['error'])
            return None

        if response.get('pStatus'):
            st.success(f"Welcome, {response['pRestaurantUserName']}!")
            st.info(response['pStatusCheck'])
        else:
            st.error("Authentication failed.")
            st.warning(response.get('pStatusCheck', "No status check available."))


