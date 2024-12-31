import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database configuration
DB_HOST = '192.95.14.153'
DB_USER = 'webbuilderuser'
DB_PASSWORD = 'm7xXGk6scyBv1iPORvmJ'
DB_NAME = 'Rest'

# Function to Connect MySQL Database : Rest
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            st.success("Successfully Connected to MySQL Database : Rest!")
            return connection
        else:
            st.error("Failed to Connect to MySQL Database : Rest!")
            return None
    except Error as e:
        st.error(f"Error : {e}")
        return None

# Function to Execute Stored Procedure Passing IN and Retrieving OUT Parameters
def execute_stored_procedure(stored_procedure_name, in_params):
    try:
        connection = connect_to_db()
        if connection is not None:
            cursor = connection.cursor()

            # Define OUT variables
            cursor.execute("SET @pRestaurantUserName = '';")
            cursor.execute("SET @pStatus = 0;")
            cursor.execute("SET @pStatusCheck = '';")

            # Construct the procedure call query
            call_query = (
                f"CALL {stored_procedure_name}("
                f"'{in_params[0]}', '{in_params[1]}', '{in_params[2]}', "
                f"@pRestaurantUserName, @pStatus, @pStatusCheck);"
            )
            cursor.execute(call_query)

            # Retrieve OUT parameters
            cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
            out_values = cursor.fetchone()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            # Return OUT parameters
            return {
                "pRestaurantUserName": out_values[3],
                "pStatus": bool(out_values[4]),
                "pStatusCheck": out_values[5],
            }
        else:
            st.error("Unable to Execute Stored Procedure, Database Connection Failed.")
            return None
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Streamlit UI
st.title("MySQL Database Connection and Stored Procedure Testing")

# Execute the Stored Procedure when the Button is Pressed / Clicked
# if st.button("Test Stored Procedure"):
#     stored_procedure_name = "RestaurantSignin"
#     restaurant = "KhanRestaurant"
#     restaurant_user = "03004444001"
#     restaurant_user_password = "abcd"
#     # IN parameters
#     in_params = [
#         restaurant,
#         restaurant_user,
#         restaurant_user_password
#     ]

#     # Execute the stored procedure and get OUT parameters
#     result = execute_stored_procedure(stored_procedure_name, in_params)
    
#     if result:
#         # Display OUT Parameters (if received)
#         st.write(f"pRestaurantUserName: {result['pRestaurantUserName']}")
#         st.write(f"pStatus: {result['pStatus']}")
#         st.write(f"pStatusCheck: {result['pStatusCheck']}")

if st.button("Test Stored Procedure"):
    stored_procedure_name = "RestaurantSignin"
    
    # IN parameters
    in_params = [
        "KhanBurger",  # Replace with actual restaurant name
        "03004444001",        # Replace with actual user name
        "abcd"     # Replace with actual password
    ]

    # Execute the stored procedure
    result = execute_stored_procedure(stored_procedure_name, in_params)

    # Check if result is not None
    st.write(f"Result : {result}")
    if result:
        # Display OUT parameters
        st.write(f"pRestaurantUserName: {result['pRestaurantUserName']}")
        st.write(f"pStatus: {result['pStatus']}")
        st.write(f"pStatusCheck: {result['pStatusCheck']}")
    else:
        st.error("Failed to execute stored procedure or retrieve results.")
