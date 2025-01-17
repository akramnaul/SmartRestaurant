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
    # Initialize the list of restaurants
    if 'list_of_restaurants' not in st.session_state:
        st.session_state['list_of_restaurants'] = [
            ("FinePizza", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
            ("HajiRestaurant", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
            ("HotNSpicy", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
            ("KhanBurger", "Guldasht Town, Zarrar Shaheed Road, Lahore"),
        ]

    # Function to generate random colors
    def get_random_color():
        return f"#{random.randint(0, 0xFFFFFF):06x}"

    # Render buttons with unique colors for each restaurant
    st.title("Choose Your Restaurant:")

    # Display buttons for each restaurant
    for restaurant, restaurant_address in st.session_state['list_of_restaurants']:
        button_color = get_random_color()  # Generate a unique color for each button
        
        # Display the button with custom CSS to change the background color
        button_html = f"""
        <style>
            .button-{restaurant} {{
                background-color: {button_color};
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 16px;
                margin: 10px 5px;
                cursor: pointer;
                border-radius: 5px;
                width: 100%;
            }}
            .button-{restaurant}:hover {{
                background-color: #333333;
            }}
        </style>
        <button class="button-{restaurant}">{restaurant} ({restaurant_address})</button>
        """

        # Render the button using markdown
        st.markdown(button_html, unsafe_allow_html=True)

        # Handle button click (using Streamlit buttons)
        if st.button(f"Select {restaurant}"):
            st.session_state.selected_restaurant = {
                "Restaurant": restaurant,
                "Address": restaurant_address,
            }
            st.success(f"You Selected: Restaurant: '{restaurant}' (Address: '{restaurant_address}')")
            st.stop()

    # Warning message if no restaurant is selected
    if 'selected_restaurant' not in st.session_state:
        st.warning("Please select a restaurant.")















        
        
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
