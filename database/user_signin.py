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


# Verify a Valid User Signin
def verify_valid_user_signin():
    # Check if 'signin_required_fields' exists and validate all required fields / values
    if 'signin_required_fields' not in st.session_state:
        st.error("Sign-in Configuration is Missing ! ")
        return False
    # Validate all required fields and check the sign-in validation flag
    if all(st.session_state.get(field) for field in st.session_state['signin_required_fields']) and \
            st.session_state.get('RestaurantUserSigninValid', False):
        st.success("Sign-in is valid!")
        return True
    else:
        st.error("Sign-in is not valid!")
        return False



# Setup Session Variables
def setup_session_variables():
    # Create and Initialize the list of restaurants in the session with names and addresses
    st.session_state.setdefault('list_of_restaurants', [
        ("FinePizza", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
        ("HajiRestaurant", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
        ("HotNSpicy", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
        ("KhanBurger", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
    ])

    # Set the list of required fields for sign-in validation
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
    st.session_state.setdefault('RestaurantUserSigninValid', None)


# Main function to render the app
def user_signin():
verify_valid_user_signin():    # Validate required fields for signin
    signin_required_fields = [
        'Restaurant', 'RestaurantUser', 'RestaurantUserPassword',
        'RestaurantUserName', 'RestaurantUserClass', 'RestaurantUserAddress'
    ]
    if all(st.session_state.get(field) for field in signin_required_fields):
        st.session_state['RestaurantUserSigninValid'] = True
        st.success("Sign-in successful!")
        st.stop()  # Stop execution to avoid rendering the restaurant selection

    # Render restaurant selection
    st.title("Smart Restaurant")
    
    # Create a list of restaurant display names (name and address combined)
    restaurant_options = [
        f"{restaurant} ({address})" 
        for restaurant, address in st.session_state['list_of_restaurants']
    ]
    
    # Set a default restaurant (e.g., the first restaurant in the list)
    default_selection = restaurant_options[3]  # 3 : KhanBurger : You can change this to any specific restaurant
    
    # Display the selectbox for restaurant selection
    selected_option = st.selectbox(
        "",
        options=["Select..."] + restaurant_options,
        index=0  # The index 0 corresponds to "Select..." as the default
    )
    
    # Handle selection or default
    if selected_option != "Select...":
        # Extract the restaurant name and address from the selected option
        for restaurant, address in st.session_state['list_of_restaurants']:
            if selected_option == f"{restaurant} ({address})":
                st.session_state['selected_restaurant'] = {
                    "Restaurant": restaurant,
                    "Address": address,
                }
                st.success(f"My Choice : '{restaurant}' ('{address}')")
                st.stop()  # Stop further rendering after a selection is made
    else:
        # Handle the default scenario
        default_restaurant, default_address = st.session_state['list_of_restaurants'][3]
        st.session_state['selected_restaurant'] = {
            "Restaurant": default_restaurant,
            "Address": default_address,
        }
        st.info(f": '{default_restaurant}' ('{default_address}')")

    # Add fields to get ID and Password from the user
    st.subheader("Enter Your Credentials")
    
    # Display placeholder in the User ID input field
    user_id = st.text_input("", placeholder="Enter Mobile Number")  # Placeholder text for the input field
    user_password = st.text_input("", type="password", placeholder="Enter Password")

    if st.button("Sign In"):
        if user_id and user_password:
            st.session_state['user_id'] = user_id
            st.session_state['user_password'] = user_password
            st.success("Sign-in successful with the provided credentials!")
            st.stop()
        else:
            st.error("Please provide both User ID and Password.")
