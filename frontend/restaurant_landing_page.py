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
def validate_user(restaurant, restaurant_user, restaurant_user_password):
    try:
        stored_procedure_name = "RestaurantSignin"
        stored_procedure_call = (
            f"CALL {stored_procedure_name}("
            f"'{restaurant}', '{restaurant_user}', '{restaurant_user_password}', "
            f"@pRestaurantUserName, @pRestaurantUserClass, @pRestaurantUserAddress, @pStatus, @pStatusCheck);"
        )
        out_parameters_query = (
            "SELECT @pRestaurantUserName, @pRestaurantUserClass, "
            "@pRestaurantUserAddress, @pStatus, @pStatusCheck;"
        )
        result = execute_stored_procedure(stored_procedure_call, out_parameters_query)
        return result
    except Error as e:
        st.error(f"An error occurred while validating user: {e}")
        return None

# Main function to render the app
def signin():
    if "selected_restaurant" not in st.session_state:
        st.session_state.selected_restaurant = None
    if "user_details" not in st.session_state:
        st.session_state.user_details = None
    if "list_of_restaurants" not in st.session_state:
        st.session_state.list_of_restaurants = fetch_list_of_restaurants()

    list_of_restaurants = st.session_state.list_of_restaurants

    # Step 1: Restaurant Selection
    if not st.session_state.selected_restaurant:
        st.title("Choose Your Restaurant")
        if list_of_restaurants:
            st.subheader("Available Restaurants")
            for restaurant, restaurant_address in list_of_restaurants:
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

    # Step 2: User Login
    st.title("User Login")
    selected_restaurant = st.session_state.selected_restaurant
    st.write(f"Selected Restaurant: **{selected_restaurant['Restaurant']}**")
    restaurant_user = st.text_input("Enter Your Mobile Number")
    restaurant_user_password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if not restaurant_user or not restaurant_user_password:
            st.error("Please provide both User Mobile Number and Password.")
        else:
            user_details = validate_user(
                selected_restaurant["Restaurant"], restaurant_user, restaurant_user_password
            )
            if user_details and len(user_details) == 5:
                st.session_state.user_details = {
                    "Name": user_details[0],
                    "Class": user_details[1],
                    "Address": user_details[2],
                    "Status": user_details[3],
                    "StatusCheck": user_details[4],
                }
                st.success("Login successful!")
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
