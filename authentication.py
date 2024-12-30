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
        # Establish database connection
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Initialize OUT parameter placeholders
        cursor.execute("SET @pRestaurantUserName = NULL;")
        cursor.execute("SET @pStatus = NULL;")
        cursor.execute("SET @pStatusCheck = NULL;")

        # Call the stored procedure
        cursor.callproc('RestaurantSignin', [restaurant, user, password, '@pRestaurantUserName', '@pStatus', '@pStatusCheck'])

        # Fetch OUT parameter values
        cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
        out_params = cursor.fetchone()

        # Debugging: Log the OUT parameters
        print(f"DEBUG: OUT Parameters: {out_params}")

        # Process and return results
        if out_params:
            pRestaurantUserName = out_params[0] if out_params[0] else "Unknown"
            pStatus = bool(out_params[1]) if out_params[1] is not None else False
            pStatusCheck = out_params[2] if out_params[2] else "No status check available"

            return {
                'pRestaurantUserName': pRestaurantUserName,
                'pStatus': pStatus,
                'pStatusCheck': pStatusCheck
            }
        else:
            return {
                'error': 'Stored procedure executed but returned no data.',
                'pRestaurantUserName': None,
                'pStatus': False,
                'pStatusCheck': "No status check available"
            }

    except mysql.connector.Error as err:
        print(f"DEBUG: MySQL error: {str(err)}")
        return {'error': f"MySQL error: {str(err)}"}
    except Exception as e:
        print(f"DEBUG: Unexpected error: {str(e)}")
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
