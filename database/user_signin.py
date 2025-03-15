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
    # Create a list of restaurant display names (name and address combined)
    restaurant_options = [
        f"{restaurant} ({address})" 
        for restaurant, address in st.session_state['list_of_restaurants']
    ]

    # Set a default restaurant (e.g., the first restaurant in the list)
    # default_selection = restaurant_options[0]  # 3 : KhanBurger : You can change this to any specific restaurant

    # Display the selectbox for restaurant selection
    selected_option = st.selectbox(
        "",
        options=["Select Restaurant ..."] + restaurant_options,
        index=0  # The index 0 corresponds to "Select..." as the default
    )
    
    # Handle selection or default
    if selected_option != "Select Restaurant ...":
        # Extract the restaurant name and address from the selected option
        for restaurant, address in st.session_state['list_of_restaurants']:
            if selected_option == f"{restaurant} ({address})":
                st.session_state['selected_restaurant'] = {
                    "Restaurant": restaurant,
                    "Address": address,
                }
                # st.success(f"My Choice : '{restaurant}' ('{address}')")
                # st.stop()  # Stop further rendering after a selection is made
    else:
        pass

    pRestaurant = st.session_state.get(['selected_restaurant'],[0])

    # Add fields to get ID and Password from the user
    st.subheader("Enter Your Credentials")
    
    # Display placeholder in the User ID input field
    pRestaurantUser = st.text_input("", placeholder="Enter Mobile Number")  # Placeholder text for the input field
    pRestaurantUserPassword = st.text_input("", type="password", placeholder="Enter Password")

    if st.button("Sign In"):
        if pRestaurant and pRestaurantUser and pRestaurantUserPassword:
            st.session_state['Restaurant'] = pRestaurant
            st.session_state['RestaurantUser'] = pRestaurantUser
            st.session_state['RestaurantUserPassword'] = pRestaurantUserPassword
            # st.success("Sign-in successful with the provided credentials!")
            # st.stop()
        else:
            st.error("Please select restaurant and provide ID and Password.")

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
        # st.write(f"'{pRestaurantUserName or ''}', '{pRestaurantUserClass or ''}', '{pRestaurantUserAddress or ''}', '{pStatus or ''}', '{pStatusCheck or ''}'")
        return result
    except Error as e:
        st.error(f"Error Signing in ..... {e}..... ")
        return None

    st.subheader("Smart Restaurant : Fresh Signin Success")


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
