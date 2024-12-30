import streamlit as st
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def authenticate_user(restaurant, user, password):
    """
    Authenticate a user by calling the RestaurantSignin stored procedure.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Update with your DB host
            user="root",       # Update with your DB user
            password="password",  # Update with your DB password
            database="restaurant_db"  # Update with your DB name
        )
        cursor = conn.cursor()

        # Set output parameters
        cursor.execute("SET @pRestaurantUserName = NULL;")
        cursor.execute("SET @pStatus = NULL;")
        cursor.execute("SET @pStatusCheck = NULL;")

        # Call the stored procedure
        cursor.callproc("RestaurantSignin", [
            restaurant, user, password,
            '@pRestaurantUserName', '@pStatus', '@pStatusCheck'
        ])

        # Fetch output parameters
        cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
        out_params = cursor.fetchone()

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
        return {'error': f"MySQL error: {err}"}
    except Exception as e:
        return {'error': f"Unexpected error: {e}"}
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
        elif response.get('pStatus'):
            st.success(f"Welcome, {response['pRestaurantUserName']}!")
            st.info(response['pStatusCheck'])
        else:
            st.error("Authentication failed.")
            st.warning(response.get('pStatusCheck', "No status check available."))

if __name__ == "__main__":
    render_authentication_ui()
