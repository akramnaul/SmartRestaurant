# Check the code :
# restaurant_landing_page.py
import streamlit as st
from mysql.connector import Error
from dotenv import load_dotenv
import os 
from database.connect_database import connect_database
from database.stored_procedures import execute_stored_procedure

# Load environment variables (if needed for database credentials)
load_dotenv()

# Helper function to fetch list of Restaurants from the Database
def fetch_list_of_restaurants():
    try:
        connection = connect_database()
        if not connection:
            st.error("Database Connection Failed.")
            return []

        query = "SELECT Restaurant FROM Restaurant;"
        with connection.cursor() as cursor:
            cursor.execute(query)
            list_of_restaurants = [row[0] for row in cursor.fetchall()]
        return list_of_restaurants

    except Error as e:
        st.error(f"An Error Occurred: {e}")
        return []

    finally:
        if connection and connection.is_connected():
            connection.close()

# Function to validate user credentials, sign in, and fetch user details
def validate_user(restaurant, restaurant_user, restaurant_user_password):
    try:
        stored_procedure_name = "RestaurantSignin"
        stored_procedure_call = (
            f"CALL {stored_procedure_name}("
            f"'{restaurant}', '{restaurant_user}', '{restaurant_user_password}',"  # IN Parameters
            f"@pRestaurantUserName, @pRestaurantUserClass, @pRestaurantUserAddress, @pStatus, @pStatusCheck);"  # OUT Parameters
        )
        out_parameters_query = (
            "SELECT @pRestaurantUserName, @pRestaurantUserClass, "
            "@pRestaurantUserAddress, @pStatus, @pStatusCheck;"
        )

        # Execute the stored procedure and fetch output parameters
        result = execute_stored_procedure(stored_procedure_call, out_parameters_query)
        return result

    except Error as e:
        st.error(f"An error occurred while validating user: {e}")
        return None

# Main function to render the app
def signin():
    # Check if session state variables exist, if not initialize those
    if "selected_restaurant" not in st.session_state:
        st.session_state.selected_restaurant = None
    if "user_details" not in st.session_state:
        st.session_state.user_details = None

    # Step 1: Restaurant Selection
    if not st.session_state.selected_restaurant:
        st.title("Choose Your Restaurant")
        list_of_restaurants = fetch_list_of_restaurants()

        if list_of_restaurants:
            st.subheader("Available Restaurants")
            for restaurant in list_of_restaurants:
                if st.button(restaurant):
                    st.session_state.selected_restaurant = restaurant
                    st.success(f"Restaurant '{restaurant}' selected!")
                    st.experimental_rerun()
        else:
            st.warning("No Restaurants Available.")
        return

    # Step 2: User Login
    st.title("User Login")
    st.write(f"Selected Restaurant: **{st.session_state.selected_restaurant}**")

    restaurant_user = st.text_input("Enter Your Mobile Number")
    restaurant_user_password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if not restaurant_user or not restaurant_user_password:
            st.error("Please provide both User Mobile Number and Password.")
        else:
            user_details = validate_user(
                st.session_state.selected_restaurant, restaurant_user, restaurant_user_password
            )

            if user_details:
                st.session_state.user_details = {
                    "Name": user_details[0],
                    "Class": user_details[1],
                    "Address": user_details[2],
                    "Status": user_details[3],
                    "StatusCheck": user_details[4],
                }
                st.success("Login successful!")
                st.write("User Details:")
                st.write(f"Name: {user_details[0]}")
                st.write(f"Class: {user_details[1]}")
                st.write(f"Address: {user_details[2]}")
                st.write(f"Status: {user_details[3]}")
                st.write(f"StatusCheck: {user_details[4]}")
            else:
                st.error("Invalid credentials or an error occurred.")












# # Stored Procedure User Interface
# def stored_procedure_ui():
#     st.title("MySQL Database Interaction")

#     try:
#         # Attempt to connect to the database
#         connection = connect_database()
#         if connection is not None:
#             st.success("Successfully Connected MySQL Database : Rest !")

#             # Define Stored Procedure Name &  IN Parameters
#             stored_procedure_name = "RestaurantSignin"
#             pRestaurant = "KhanBurger"
#             pRestaurantUser = "03004444001"
#             pRestaurantUserPassword = "abcd"
#             stored_procedure_button = "Click 2 Test"
            
#             # Button to Trigger the Stored Procedure
#             if st.button(f"{stored_procedure_button} : {stored_procedure_name}"):
#                 # Build the Stored Procedure Call String
#                 stored_procedure_call = (
#                     f"CALL {stored_procedure_name}("
#                     f"'{pRestaurant}', '{pRestaurantUser}', '{pRestaurantUserPassword}',"                              # IN Parameters
#                     f"@pRestaurantUserName, @pRestaurantUserClass, @pRestaurantUserAddress, @pStatus, @pStatusCheck);" # OUT Parameters
#                 )
#                 stored_procedure_out_parameters = "SELECT @pRestaurantUserName, @pRestaurantUserClass, @pRestaurantUserAddress, @pStatus, @pStatusCheck;"
#                 # Show loading indicator
#                 with st.spinner("Executing Stored Procedure....."):
#                     # Execute the stored procedure
#                     returning_out_parameters = execute_stored_procedure(stored_procedure_call,stored_procedure_out_parameters)

#                     # Display the results
#                     if returning_out_parameters:
#                         st.write("Stored Procedure Output Parameters:")
#                         st.write(f"pRestaurantUserName : {returning_out_parameters[0]}")
#                         st.write(f"pRestaurantUserClass : {returning_out_parameters[1]}")
#                         st.write(f"pRestaurantUserAddress : {returning_out_parameters[2]}")
#                         st.write(f"pStatus : {bool(returning_out_parameters[3])}")
#                         st.write(f"pStatusCheck : {returning_out_parameters[4]}")
#                     else:
#                         st.error("Failed to execute the stored procedure or retrieve results.")
#         else:
#             st.error("Failed to Connect to the Database. Please Check the Connection Details.....")

#     except Error as e:
#         st.error(f"An Error Occurred While Interacting with the Database: {e}")
