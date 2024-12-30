import streamlit as st
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def authenticate_user(restaurant, user, password):
    """
    Authenticate a user by calling the RestaurantSignin Stored Procedure.
    
    Args:
        restaurant (str): Restaurant name.
        user (str): User name.
        password (str): User password.

    Returns:
        dict: OUT parameters from the Stored Procedure : @pRestaurantUserName, @pStatus (BOOLEAN), @pStatusCheck
    """
    conn = None
    cursor = None
    try:
        # Establish the connection
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Define OUT Parameter Variables
        cursor.execute("SET @pRestaurantUserName = NULL;")
        cursor.execute("SET @pStatus = NULL;")  # BOOLEAN type, should be TRUE or FALSE
        cursor.execute("SET @pStatusCheck = NULL;")

        # Call the stored procedure
        cursor.callproc('RestaurantSignin', [
            restaurant, user, password,
            '@pRestaurantUserName', '@pStatus', '@pStatusCheck'
        ])

        # Fetch the OUT parameters
        cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
        result = cursor.fetchone()

        # Debug: Log the raw result
        print(f"DEBUG: Raw result from stored procedure: {result}")

        # Validate and return results
        if result:
            return {
                'pRestaurantUserName': result[0] or "Unknown",
                'pStatus': bool(result[1]) if result[1] is not None else False,  # Convert to BOOLEAN
                'pStatusCheck': result[2] or "No status check available"
            }
        else:
            # Debug: Include raw result in the error message
            return {
                'error': 'Procedure executed but returned incomplete or null values.',
                'raw_result': result,
                'pRestaurantUserName': result[0] if result else None,
                'pStatus': result[1] if result else None,
                'pStatusCheck': result[2] if result else None
            }

    except mysql.connector.Error as err:
        return {'error': f"MySQL error: {str(err)}"}
    except Exception as e:
        return {'error': f"Unexpected error: {str(e)}"}

    finally:
        # Ensure cleanup
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Streamlit UI for authentication
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

        if response['pStatus']:
            st.success(f"Welcome, {response['pRestaurantUserName']}!")
            st.info(response['pStatusCheck'])
            return response  # Successful authentication
        else:
            st.warning("Authentication failed.")
            st.info(response['pStatusCheck'])
            return None  # Failed authentication
