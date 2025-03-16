# Check the code :
# user_signin.py
import streamlit as st
import random
from mysql.connector import Error
from dotenv import load_dotenv
import os
from database.connect_database import connect_database
from database.execute_stored_procedure import execute_stored_procedure

# Load environment variables
load_dotenv()


# Setup Session Variables
def setup_new_session():
    # Create and Initialize the list of restaurants in the session with names and addresses
    # if ('list_of_restaurants' not in st.session_state):
    st.session_state.setdefault('list_of_restaurants', [
        # ("FinePizza", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
        # ("HajiRestaurant", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
        # ("HotNSpicy", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
        ("KhanBurger", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
        ("KhanBurger", "Gulberg, Lahore"),
    ])

    # Set the list of required fields for sign-in validation
    # if ('signin_required_fields' not in st.session_state):
    st.session_state.setdefault('signin_required_fields', [
        'Restaurant', 'RestaurantUser', 'RestaurantUserPassword',
        'RestaurantUserName', 'RestaurantUserClass', 'RestaurantUserAddress',
        'RestaurantUserSigninValid'
    ])

    # Initialize all variables in signin_required_fields with None
    st.session_state.setdefault('Restaurant', None)
    st.session_state.setdefault('RestaurantUser', None)
    st.session_state.setdefault('RestaurantUserPassword', None)
    st.session_state.setdefault('RestaurantUserName', None)
    st.session_state.setdefault('RestaurantUserClass', None)
    st.session_state.setdefault('RestaurantUserAddress', None)
    st.session_state.setdefault('RestaurantUserSigninValid', False)

    st.subheader("Smart Restaurant : New Session Success")


# Function to validate user credentials
def user_signin_afresh():
    restaurant_options = [
        f"{restaurant} ({address})" 
        for restaurant, address in st.session_state.get('list_of_restaurants', [])
    ]

    selected_option = st.selectbox(
        # "Select Restaurant",
        # options=["Select Restaurant ..."] + restaurant_options,
        options=restaurant_options, # ["Select Restaurant ..."] + 
        index=0
    )

    # if selected_option != "Select Restaurant ...":
    for restaurant, address in st.session_state.get('list_of_restaurants', []):
        if selected_option == f"{restaurant} ({address})":
            st.session_state['selected_restaurant'] = {
                "Restaurant": restaurant,
                "Address": address,
            }

    # ✅ Fixing session state access
    pRestaurant = st.session_state.get('selected_restaurant', [])

    st.subheader("Enter Your Credentials")
    pRestaurantUser = st.text_input("", placeholder="Enter Mobile Number")
    pRestaurantUserPassword = st.text_input("", type="password", placeholder="Enter Password")

    if st.button("Sign In"):
        if pRestaurant and pRestaurantUser and pRestaurantUserPassword:
            st.session_state['Restaurant'] = pRestaurant
            st.session_state['RestaurantUser'] = pRestaurantUser
            st.session_state['RestaurantUserPassword'] = pRestaurantUserPassword
        else:
            st.error("Please select a restaurant and provide ID and Password.")
            return None  # ✅ Stop execution if inputs are missing

        try:
            StoredProcedureName = "RestaurantSignin"
            StoredProcedureCall = (
                f"CALL {StoredProcedureName}("
                f"'{pRestaurant}', '{pRestaurantUser}', '{pRestaurantUserPassword}', "
                f"@pRestaurantUserName, @pRestaurantUserClass, @pRestaurantUserAddress, @pStatus, @pStatusCheck);"
            )
            OutParametersQuery = (
                "SELECT @pRestaurantUserName, @pRestaurantUserClass, @pRestaurantUserAddress, @pStatus, @pStatusCheck;"
            )
            result = execute_stored_procedure(StoredProcedureCall, OutParametersQuery)

            if result:
                pRestaurantUserName, pRestaurantUserClass, pRestaurantUserAddress, pStatus, pStatusCheck = result
                st.write(f"'{pRestaurantUserName}', '{pRestaurantUserClass}', '{pRestaurantUserAddress}', '{pStatus}', '{pStatusCheck}'")
                st.subheader("Smart Restaurant : Fresh Signin Success")  # ✅ Now it will execute
            else:
                st.error("Error: No data returned from the database.")
            return result
        except Error as e:
            st.error(f"Error Signing in: {e}")
            return None


# Main function to render the app
def user_signin():
    # Check if 'RestaurantUserSigninValid' exists and True
    if (('RestaurantUserSigninValid' in st.session_state) and (st.session_state['RestaurantUserSigninValid'] is True)):
        st.subheader("Smart Restaurant : Previous Valid Session & Signin")
        return True
    else:
        st.subheader("Smart Restaurant : New Session & Signin")
        setup_new_session()
        user_signin_afresh()
