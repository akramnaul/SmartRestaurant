import streamlit as st
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def authenticate_user(restaurant, user, password):
    try:
        conn = mysql.connector.connect(
            host="localhost",   # or IP address of your MySQL server
            user="your_user",   # your MySQL username
            password="your_password",  # your MySQL password
            database="your_database"  # your database name
        )

        cursor = conn.cursor()

        # Set initial OUT parameters
        cursor.execute("SET @pRestaurantUserName = NULL;")
        cursor.execute("SET @pStatus = NULL;")
        cursor.execute("SET @pStatusCheck = NULL;")

        # Execute the stored procedure
        cursor.callproc('RestaurantSignin', [
            restaurant, user, password,
            '@pRestaurantUserName', '@pStatus', '@pStatusCheck'
        ])

        # Fetch the result
        cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
        result = cursor.fetchone()

        print(f"DEBUG: Raw result: {result}")

        if result:
            pRestaurantUserName = result[0] if result[0] else "Unknown"
            pStatus = result[1] if result[1] is not None else 0
            pStatusCheck = result[2] if result[2] else "No status check available"

            print(f"DEBUG: Processed result - pRestaurantUserName: {pRestaurantUserName}, pStatus: {pStatus}, pStatusCheck: {pStatusCheck}")
            return {
                'pRestaurantUserName': pRestaurantUserName,
                'pStatus': pStatus,
                'pStatusCheck': pStatusCheck
            }
        else:
            print("DEBUG: No result returned from stored procedure.")
            return {'error': 'No result returned from stored procedure.'}

    except mysql.connector.Error as err:
        print(f"DEBUG: MySQL Error: {err}")
        return {'error': f"MySQL error: {str(err)}"}

    except Exception as e:
        print(f"DEBUG: Unexpected Error: {e}")
        return {'error': f"Unexpected error: {str(e)}"}

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()






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
