import streamlit as st
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def authenticate_user(restaurant, user, password):
    """
    Authenticate a user by calling the RestaurantSignin Stored Procedure.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Call stored procedure with OUT parameters
        cursor.callproc('RestaurantSignin', [
            restaurant, user, password, None, None, None
        ])

        # Fetch results
        for result in cursor.stored_results():
            out_params = result.fetchone()

        if out_params:
            return {
                'pRestaurantUserName': out_params[0],
                'pStatus': bool(out_params[1]),
                'pStatusCheck': out_params[2]
            }
        else:
            return {'error': 'No data returned from stored procedure.'}

    except mysql.connector.Error as err:
        return {'error': f"MySQL error: {str(err)}"}
    except Exception as e:
        return {'error': f"Unexpected error: {str(e)}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def render_authentication_ui():
    """
    Streamlit UI for user authentication.
    """
    st.subheader("Restaurant Signin")

    with st.form("signin_form"):
        restaurant = st.text_input("Restaurant Name")
        user = st.text_input("User Name")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Signin")

    if submitted:
        if not restaurant or not user or not password:
            st.error("All fields are required.")
            return None

        response = authenticate_user(restaurant, user, password)

        if 'error' in response:
            st.error(response['error'])
            return None

        if response.get('pStatus'):
            st.success(f"Welcome, {response['pRestaurantUserName']}!")
            st.info(response['pStatusCheck'])
            return response
        else:
            st.warning("Authentication failed.")
            st.info(response.get('pStatusCheck'))
            return None
