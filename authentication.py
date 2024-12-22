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
        dict: OUT parameters from the stored procedure.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Define OUT parameters
        pRestaurantUserName = ''
        pStatus = 0
        pStatusCheck = ''

        # Call the stored procedure
        cursor.callproc('RestaurantSignin', [
            restaurant, user, password,
            pRestaurantUserName, pStatus, pStatusCheck
        ])

        # Fetch OUT parameters
        for result in cursor.stored_results():
            # Extract OUT parameters from the result
            result_data = result.fetchall()

        cursor.close()
        conn.close()

        # Return a dictionary with OUT parameters
        return {
            'pRestaurantUserName': pRestaurantUserName,
            'pStatus': pStatus,
            'pStatusCheck': pStatusCheck
        }

    except mysql.connector.Error as err:
        return {'error': str(err)}

# Streamlit UI for authentication
def main():
    st.title("Restaurant Sign-In")

    with st.form("signin_form"):
        restaurant = st.text_input("Restaurant Name", help="Enter your restaurant's name.")
        user = st.text_input("User Name", help="Enter your username.")
        password = st.text_input("Password", type="password", help="Enter your password.")
        submitted = st.form_submit_button("Sign In")

    if submitted:
        if not restaurant or not user or not password:
            st.error("All fields are mandatory.")
            return

        # Call the authentication function
        response = authenticate_user(restaurant, user, password)

        if 'error' in response:
            st.error(f"Database error: {response['error']}")
        else:
            pRestaurantUserName = response['pRestaurantUserName']
            pStatus = response['pStatus']
            pStatusCheck = response['pStatusCheck']

            if pStatus:
                st.success(f"Welcome, {pRestaurantUserName}!")
                st.info(pStatusCheck)
                # Proceed with registered user operations
                st.write("Proceeding with registered user operations...")
            else:
                st.warning("Authentication failed.")
                st.info(pStatusCheck)
                # Proceed with unregistered user operations
                st.write("Proceeding with unregistered user operations...")

if __name__ == "__main__":
    main()
