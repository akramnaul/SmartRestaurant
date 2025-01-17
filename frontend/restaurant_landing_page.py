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
    # Initialize the list of restaurants with names and addresses
    if 'list_of_restaurants' not in st.session_state:
        st.session_state['list_of_restaurants'] = [
            ("FinePizza", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
            ("HajiRestaurant", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
            ("HotNSpicy", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
            ("KhanBurger", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
        ]

    # Render buttons for each restaurant
    st.title("Choose Your Restaurant:")
    # If no restaurant is selected yet
    # if 'selected_restaurant' not in st.session_state:
    #     st.warning("Please select a restaurant.")

    # Loop through the list of restaurants and create buttons with both name and address
    for restaurant, restaurant_address in st.session_state['list_of_restaurants']:
        button_label = f"{restaurant} ({restaurant_address})"
        if st.button(button_label):
            st.session_state.selected_restaurant = {
                "Restaurant": restaurant,
                "Address": restaurant_address,
            }
            st.success(f"You Selected: Restaurant: '{restaurant}' (Address: '{restaurant_address}')")
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

    
    # List of Registered Restaurants
    list_of_restaurants = ["FinePizza", "HajiRestaurant", "HotNSpicy", "KhanBurger"]

    
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
