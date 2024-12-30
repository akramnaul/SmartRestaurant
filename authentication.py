import streamlit as st
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

import mysql.connector

def authenticate_user(restaurant, user, password):
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

        # Initialize OUT parameters
        cursor.execute("SET @pRestaurantUserName = NULL;")
        cursor.execute("SET @pStatus = NULL;")
        cursor.execute("SET @pStatusCheck = NULL;")

        # Call stored procedure
        cursor.callproc('RestaurantSignin', [
            restaurant, user, password,
            '@pRestaurantUserName', '@pStatus', '@pStatusCheck'
        ])

        # Fetch the output values from the stored procedure
        cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
        result = cursor.fetchone()

        # Debug: Print the raw result from the stored procedure
        print(f"DEBUG: Raw result from stored procedure: {result}")

        if result:
            pRestaurantUserName = result[0] if result[0] else "Unknown"
            pStatus = result[1] if result[1] is not None else 0
            pStatusCheck = result[2] if result[2] else "No status check available"

            # Debug: Display final response data
            print(f"DEBUG: Returning auth response - pRestaurantUserName: {pRestaurantUserName}, pStatus: {pStatus}, pStatusCheck: {pStatusCheck}")

            return {
                'pRestaurantUserName': pRestaurantUserName,
                'pStatus': pStatus,
                'pStatusCheck': pStatusCheck
            }
        else:
            print("DEBUG: No result returned from procedure")
            return {
                'error': 'Procedure executed but returned incomplete or null values.',
                'raw_result': result
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

    pStatusCheck = result[2] if result[2] else "No status check available"

    response = authenticate_user(restaurant, user, password)

    # Debug: Log the response
    print(f"DEBUG: Authentication response: {response}")
    
    if 'error' in response:
        st.error(response['error'])
    else:
        if response.get('pStatus') == 1:
            st.success(f"Welcome, {response['pRestaurantUserName']}!")
            st.info(response['pStatusCheck'])
        else:
            st.warning("Authentication failed.")
            st.info(response['pStatusCheck'])  # Display status message from procedure




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
        elif response.get('pStatus'):
            st.success(f"Welcome, {response['pRestaurantUserName']}!")
            st.info(response['pStatusCheck'])
        else:
            st.error("Authentication failed.")
            st.warning(response.get('pStatusCheck', "No status check available."))

if __name__ == "__main__":
    render_authentication_ui()
