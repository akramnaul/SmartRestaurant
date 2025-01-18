# Check the code :
# restaurant_landing_page.py
import streamlit as st
import random
from mysql.connector import Error
from dotenv import load_dotenv
import os
from database.connect_database import connect_database
from database.execute_stored_procedure import execute_stored_procedure

# Load environment variables
load_dotenv()

# Function to validate user credentials
def validate_user(pRestaurant, pRestaurantUser, pRestaurantUserPassword):
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
        return result
    except Error as e:
        st.error(f"An error occurred while validating user: {e}")
        return None

# Main function to render the app
def user_signin():
    # Initialize the list of restaurants in the session with names and addresses
    st.session_state.setdefault('list_of_restaurants', [
        ("FinePizza", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
        ("HajiRestaurant", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
        ("HotNSpicy", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
        ("KhanBurger", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
    ])
    st.session_state.setdefault('RestaurantUserSignin', False)

    # Validate required fields for sign-in
    required_fields = [
        'Restaurant', 'RestaurantUser', 'RestaurantUserPassword',
        'RestaurantUserName', 'RestaurantUserClass', 'RestaurantUserAddress'
    ]
    if all(st.session_state.get(field) for field in required_fields):
        st.session_state['RestaurantUserSignin'] = True
        st.success("Sign-in successful!")
        st.stop()  # Stop execution to avoid rendering the restaurant buttons

    # Render restaurant selection
    st.title("Choose Restaurant:")
    for restaurant, restaurant_address in st.session_state['list_of_restaurants']:
        button_label = f"{restaurant} ({restaurant_address})"
        if st.button(button_label):
            st.session_state['selected_restaurant'] = {
                "Restaurant": restaurant,
                "Address": restaurant_address,
            }
            st.success(f"You Selected : Restaurant : '{restaurant}' (Address : '{restaurant_address}')")
            st.stop()  # Stop the loop after a selection is made


        # try:
        #     StoredProcedureName        = "RestaurantSignin"
        #     pRestaurant                = st.session_state['Restaurant']
        #     pRestaurantUser            = st.session_state['RestaurantUser']
        #     pRestaurantUserPassword    = st.session_state['RestaurantUserPassword']
        #     StoredProcedureCall = (
        #         f"CALL {StoredProcedureName}("
        #         f"'{pRestaurant}', '{pRestaurantUser}', '{pRestaurantUserPassword}', "
        #         f"@pRestaurantUserName, @pRestaurantUserClass, @pRestaurantUserAddress, @pStatus, @pStatusCheck);"
        #     )
        #     OutParametersQuery = (
        #         "SELECT @pRestaurantUserName, @pRestaurantUserClass, @pRestaurantUserAddress, @pStatus, @pStatusCheck;"
        #     )
        #     result = execute_stored_procedure(StoredProcedureCall, OutParametersQuery)
        #     return result
        # except Error as e:
        #     st.error(f"An error occurred while validating user: {e}")
        #     return None

        # st.success("User successfully logged in!")
        # st.write(f"Welcome, {st.session_state['RestaurantUser']} from {st.session_state['Restaurant']}!")
        # return True


    
    # # Initialize session state variables only once
    # if 'Restaurant' not in st.session_state:
    #     st.session_state['Restaurant'] = None
    # if 'RestaurantUser' not in st.session_state:
    #     st.session_state['RestaurantUser'] = None
    # if 'RestaurantUserPassword' not in st.session_state:
    #     st.session_state['RestaurantUserPassword'] = None

    # # If session variables are not set, allow the user to initialize them
    # if st.session_state['Restaurant'] is None:
    #     st.session_state['Restaurant'] = st.selectbox("Select a Restaurant:", list_of_restaurants)

    # if st.session_state['RestaurantUser'] is None:
    #     st.session_state['RestaurantUser'] = st.text_input("Enter Username:", value="", key="username")

    # if st.session_state['RestaurantUserPassword'] is None:
    #     st.session_state['RestaurantUserPassword'] = st.text_input("Enter Password:", value="", type="password", key="password")

    # return False

# Reload the page from the top without clearing session variables
# st.experimental_rerun()
