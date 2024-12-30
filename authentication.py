import streamlit as st
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def authenticate_user(restaurant, user, password):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Reset OUT params
        cursor.execute("SET @pRestaurantUserName = NULL;")
        cursor.execute("SET @pStatus = NULL;")
        cursor.execute("SET @pStatusCheck = NULL;")

        # Execute stored procedure
        cursor.callproc('RestaurantSignin', [
            restaurant, user, password,
            '@pRestaurantUserName', '@pStatus', '@pStatusCheck'
        ])

        # Fetch OUT params after execution
        cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
        result = cursor.fetchone()

        print(f"DEBUG: Raw result from stored procedure: {result}")  # Log result

        if result:
            pRestaurantUserName = result[0] if result[0] else "Unknown"
            pStatus = bool(result[1]) if result[1] is not None else False
            pStatusCheck = result[2] if result[2] else "No status check available"
            return {
                'pRestaurantUserName': pRestaurantUserName,
                'pStatus': pStatus,
                'pStatusCheck': pStatusCheck
            }
        else:
            return {
                'error': 'Procedure executed but returned no result.',
                'raw_result': result
            }

    except mysql.connector.Error as err:
        return {'error': f"MySQL error: {str(err)}"}
    except Exception as e:
        return {'error': f"Unexpected error: {str(e)}"}
    finally:
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

        st.info(response['pStatusCheck'])

if __name__ == "__main__":
    render_authentication_ui()
