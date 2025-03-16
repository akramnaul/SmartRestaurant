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
        "Select Restaurant",
        options=["Select Restaurant ..."] + restaurant_options,
        index=0
    )

    if selected_option != "Select Restaurant ...":
        for restaurant, address in st.session_state.get('list_of_restaurants', []):
            if selected_option == f"{restaurant} ({address})":
                st.session_state['selected_restaurant'] = {
                    "Restaurant": restaurant,
                    "Address": address,
                }

    # ✅ Fixing session state access
    pRestaurant = st.session_state.get('selected_restaurant', {}).get('Restaurant', None)

    st.subheader("Enter Your Credentials")
    pRestaurantUser = st.text_input("", placeholder="Enter Mobile Number")
    pRestaurantUserPassword = st.text_input("", type="password", placeholder="Enter Your Password")

    if st.button("Sign In"):
        if pRestaurant and pRestaurantUser and pRestaurantUserPassword:
            pass # ✅ Proceed with Execution of Stored Procedure as User Input 3 Fields Correctly for Signin
        else:
            st.error("Select a Restaurant ... Enter Mobile Number and Password ... ")
            return None # ❌ Stop Execution as User did'nt Input 3 Fields Correctly for Signin

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
                st.write(f"'{pRestaurant}', '{pRestaurantUser}', '{pRestaurantUserPassword}'\n")
                st.write(f"'{pRestaurantUserName}', '{pRestaurantUserClass}', '{pRestaurantUserAddress}', '{pStatus}', '{pStatusCheck}'\n")

                st.session_state['Restaurant'] = pRestaurant
                st.session_state['RestaurantUser'] = pRestaurantUser
                st.session_state['RestaurantUserPassword'] = pRestaurantUserPassword
                st.session_state['pRestaurantUserName'] = pRestaurantUserName
                st.session_state['pRestaurantUserClass'] = pRestaurantUserClass
                st.session_state['pRestaurantUserAddress'] = pRestaurantUserAddress
                st.session_state['pStatus'] = pStatus
                st.session_state['pStatusCheck'] = pStatusCheck
                st.session_state['RestaurantUserSigninValid'] = True

                st.subheader("Smart Restaurant : Afresh Signin Successful")  # ✅ Afresh Signin Successful ✅ Now it will Proceed / Execute Application
            else:
                st.error("Error: No data returned from the database.") # ❌ Afresh Signin Unsuccessful
            return True
        except Error as e:
            st.error(f"Error Signing in: {e}")
            return False
    else:
        st.warning("Select a Restaurant ... Enter Mobile Number and Password ... then ... Click 'Sign In' to Continue ... ")
        st.stop()  # Stop further execution

# Main function to render the app
def user_signin():
    # Check if Session Variables 'Restaurant','RestaurantUser','RestaurantUserPassword','RestaurantUserSigninValid' Exists and True
    if (('Restaurant' in st.session_state) and ('RestaurantUser' in st.session_state) and ('RestaurantUserPassword' in st.session_state) and
        ('RestaurantUserSigninValid' in st.session_state) and (st.session_state['RestaurantUserSigninValid'] is True)):
        st.subheader("Smart Restaurant : Previous Valid Session & Signin")
        return True
    else:
        st.subheader("Smart Restaurant : New Session & Signin")
        setup_new_session()
        if(user_signin_afresh() is True):
            st.write("User Signin Afresh Successfully Reached : user_signin()")
            return True
        else:
            st.write("User Signin Afresh UnSuccessfully Reached : user_signin()")
            return False

    if(user_signin() is True):
      st.write("User Signin Successfully Reached : streamlit_app.py")
    else:
      st.write("User Signin UnSuccessfully Reached : streamlit_app.py")
    
    # Check User's Roll / Class ... then ... Redirect to Appropriate Webpage
    if (('RestaurantUser' in st.session_state) and ('RestaurantUser' in st.session_state) and
        ('RestaurantUserSigninValid' in st.session_state) and (st.session_state['RestaurantUserSigninValid'] is True)):
        st.subheader("Smart Restaurant : Previous Valid Session & Signin")
    else:
        st.subheader("Smart Restaurant : New Session & Signin")
    
    # JavaScript to Reload the Page
    def clear_page():
        st.markdown("""
            <script>
                location.reload();
            </script>
        """, unsafe_allow_html=True)
    
    # st.write("This is some content on the screen.")
    
    if st.button("Clear Screen"):
        clear_page()  # Reloads the page, effectively clearing it
