import streamlit as st
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# Function to call the RestaurantSignin stored procedure
def authenticate_user(restaurant, user, password):
    """
def authenticate_user(restaurant, user, password):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Define OUT parameter variables
        cursor.execute("SET @pRestaurantUserName = '';")
        cursor.execute("SET @pStatus = 0;")
        cursor.execute("SET @pStatusCheck = '';")

        # Call the stored procedure
        cursor.callproc('RestaurantSignin', [
            restaurant, user, password,
            '@pRestaurantUserName', '@pStatus', '@pStatusCheck'
        ])

        # Fetch the OUT parameters
        cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        print("Debugging Result:", result)  # Debug output

        if result:
            return {
                'pRestaurantUserName': result[0],
                'pStatus': result[1],
                'pStatusCheck': result[2]
            }
        else:
            return {'error': 'No result from the procedure.'}

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
