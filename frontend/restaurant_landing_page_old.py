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

# Helper function to fetch the list of restaurants
def fetch_list_of_restaurants():
    try:
        connection = connect_database()
        if not connection:
            st.error("Database Connection Failed.")
            return []
        query = "SELECT Restaurant, RestaurantAddress FROM Restaurant;"
        with connection.cursor() as cursor:
            cursor.execute(query)
            return [(row[0], row[1]) for row in cursor.fetchall()]
    except Error as e:
        st.error(f"An error occurred: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()

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
    # Check if all session variables are set : Confirm Valid Signin
    if (st.session_state['Restaurant'] is not None and
        st.session_state['RestaurantUser'] is not None and
        st.session_state['RestaurantUserPassword'] is not None and
        st.session_state['RestaurantUserName'] is not None and
        st.session_state['RestaurantUserClass'] is not None and
        st.session_state['RestaurantUserAddress'] is not None):
        st.session_state['RestaurantUserSignin'] = True
        return
    else
        if 'list_of_restaurants' not in st.session_state:
            st.session_state['list_of_restaurants'] = tuple(("FinePizza", "Guldasht Town, Zarrar Shaheed Road, Lahore"),("HajiRestaurant", "Guldasht Town, Zarrar Shaheed Road, Lahore"),("HotNSpicy", "Guldasht Town, Zarrar Shaheed Road, Lahore"),("KhanBurger"))
            # Display the read-only list
            st.write("Read-Only List of Restaurants:", st.session_state['list_of_restaurants'])

            st.title("Choose Your Restaurant From This List")
            for restaurant, restaurant_address in st.session_state['list_of_restaurants']:
                if st.button(f"{restaurant} ({restaurant_address})"):
                        st.session_state.selected_restaurant = {
                            "Restaurant": restaurant,
                            "Address": restaurant_address,
                        }
                        st.success(f"Restaurant: '{restaurant}' (Address: '{restaurant_address}') selected!")
                        st.stop()
            else:
                st.warning("No Restaurants Available.")
            return




        
        
        try:
            StoredProcedureName        = "RestaurantSignin"
            pRestaurant                = st.session_state['Restaurant']
            pRestaurantUser            = st.session_state['RestaurantUser']
            pRestaurantUserPassword    = st.session_state['RestaurantUserPassword']
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


        st.success("User successfully logged in!")
        st.write(f"Welcome, {st.session_state['RestaurantUser']} from {st.session_state['Restaurant']}!")
        return True

    
    # List of Registered Restaurants
    list_of_restaurants = ["FinePizza", "HajiRestaurant", "HotNSpicy", "KhanBurger"]

    
    # Initialize session state variables only once
    if 'Restaurant' not in st.session_state:
        st.session_state['Restaurant'] = None
    if 'RestaurantUser' not in st.session_state:
        st.session_state['RestaurantUser'] = None
    if 'RestaurantUserPassword' not in st.session_state:
        st.session_state['RestaurantUserPassword'] = None

    # If session variables are not set, allow the user to initialize them
    if st.session_state['Restaurant'] is None:
        st.session_state['Restaurant'] = st.selectbox("Select a Restaurant:", list_of_restaurants)

    if st.session_state['RestaurantUser'] is None:
        st.session_state['RestaurantUser'] = st.text_input("Enter Username:", value="", key="username")

    if st.session_state['RestaurantUserPassword'] is None:
        st.session_state['RestaurantUserPassword'] = st.text_input("Enter Password:", value="", type="password", key="password")


    return False

# Reload the page from the top without clearing session variables
# st.experimental_rerun()



    

    
    # if "selected_restaurant" not in st.session_state:
    #     st.session_state.selected_restaurant = None
    # if "user_details" not in st.session_state:
    #     st.session_state.user_details = None
    # if "list_of_restaurants" not in st.session_state:
    #     st.session_state.list_of_restaurants = fetch_list_of_restaurants()

    # list_of_restaurants = st.session_state.list_of_restaurants

    # # Step 1: Restaurant Selection
    # if not st.session_state.selected_restaurant:
    #     st.title("Choose Your Restaurant")
    #     if list_of_restaurants:
    #         st.subheader("Available Restaurants")
    #         for restaurant, restaurant_address in list_of_restaurants:
    #             if st.button(f"{restaurant} ({restaurant_address})"):
    #                 st.session_state.selected_restaurant = {
    #                     "Restaurant": restaurant,
    #                     "Address": restaurant_address,
    #                 }
    #                 st.success(f"Restaurant: '{restaurant}' (Address: '{restaurant_address}') selected!")
    #                 st.stop()
    #     else:
    #         st.warning("No Restaurants Available.")
    #     return

    # # Step 2: User Login
    # st.title("User Login")
    # selected_restaurant = st.session_state.selected_restaurant
    # st.write(f"Selected Restaurant: **{selected_restaurant['Restaurant']}**")
    # restaurant_user = st.text_input("Enter Your Mobile Number")
    # restaurant_user_password = st.text_input("Enter Password", type="password")

    # if st.button("Login"):
    #     if not restaurant_user or not restaurant_user_password:
    #         st.error("Please provide both User Mobile Number and Password.")
    #     else:
    #         user_details = validate_user(
    #             selected_restaurant["Restaurant"], restaurant_user, restaurant_user_password
    #         )
    #         if user_details and len(user_details) == 5:
    #             st.session_state.user_details = {
    #                 "Name": user_details[0],
    #                 "Class": user_details[1],
    #                 "Address": user_details[2],
    #                 "Status": user_details[3],
    #                 "StatusCheck": user_details[4],
    #             }
    #             st.success("Login successful!")
    #         else:
    #             st.error("Invalid credentials or an error occurred.")
