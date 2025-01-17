# Check the code :
# restaurant_landing_page.py
import streamlit as st
from mysql.connector import Error
from dotenv import load_dotenv
import os
from database.connect_database import connect_database
from database.execute_stored_procedure import execute_stored_procedure

# Load environment variables
load_dotenv()

# Function to validate user credentials
# def validate_user(pRestaurant, pRestaurantUser, pRestaurantUserPassword):
#     try:
#         StoredProcedureName = "RestaurantSignin"
#         StoredProcedureCall = (
#             f"CALL {StoredProcedureName}("
#             f"'{pRestaurant}', '{pRestaurantUser}', '{pRestaurantUserPassword}', "
#             f"@pRestaurantUserName, @pRestaurantUserClass, @pRestaurantUserAddress, @pStatus, @pStatusCheck);"
#         )
#         OutParametersQuery = (
#             "SELECT @pRestaurantUserName, @pRestaurantUserClass, @pRestaurantUserAddress, @pStatus, @pStatusCheck;"
#         )
#         result = execute_stored_procedure(StoredProcedureCall, OutParametersQuery)
#         return result
#     except Error as e:
#         st.error(f"An error occurred while validating user: {e}")
#         return None

# Main function to render the app
def user_signin():
    # Check if all session variables are set : Confirm Valid Signin
    if (
        st.session_state.get('list_of_restaurants') is not None and
        st.session_state.get('Restaurant') is not None and
        st.session_state.get('RestaurantUser') is not None and
        st.session_state.get('RestaurantUserPassword') is not None and
        st.session_state.get('RestaurantUserName') is not None and
        st.session_state.get('RestaurantUserClass') is not None and
        st.session_state.get('RestaurantUserAddress') is not None
    ):
        st.session_state['RestaurantUserSignin'] = True
        return
    else:
        st.session_state['list_of_restaurants'] = (
            ("FinePizza", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
            ("HajiRestaurant", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
            ("HotNSpicy", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
            ("KhanBurger", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
        )
        # Display the read-only list
        # if not st.session_state.get('selected_restaurant'):
        if st.session_state.get('list_of_restaurants') is not None
            st.title("Choose Your Restaurant From This List")
        else:
            st.warning("No Restaurants Registered / Available.")
        for restaurant, restaurant_address in st.session_state['list_of_restaurants']:
            if st.button(f"{restaurant} ({restaurant_address})"):
                st.session_state.selected_restaurant = {
                    "Restaurant": restaurant,
                    "Address": restaurant_address,
                }
                st.success(f"You Selected: Restaurant: '{restaurant}' (Address: '{restaurant_address}')")
                st.stop()
        return




        
        
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
