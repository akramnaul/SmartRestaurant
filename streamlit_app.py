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
        st.error(f"Error: {e}")
        return None

# Function to Execute Stored Procedure Passing IN and Retrieving OUT Parameters
def execute_stored_procedure(stored_procedure_name = "RestaurantSignin", pRestaurant = "KhanBurger", pRestaurantUser = "03004444001", pRestaurantUserPassword = "abcd"):
    try:
        connection = connect_to_db()
        if connection is not None:
            cursor = connection.cursor()

            # Define OUT Parameters / Variables / Equal to Pass By Reference
            cursor.execute("SET "+pRestaurantUserName+" = '';")
            cursor.execute("SET "+pStatus+" = FALSE;")
            cursor.execute("SET "+pStatusCheck+" = '';")

            # Construct the procedure call query
            call_query = (
                f"CALL {stored_procedure_name}("
                f"{pRestaurant}, {pRestaurantUser}, {pRestaurantUserPassword}, "
                f"@pRestaurantUserName, @pStatus, @pStatusCheck);"
            )
            cursor.execute(call_query)

            # Retrieve OUT Parameters / Variables / Equal to Pass By Reference
            cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
            out_parameters = cursor.fetchone()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            # Return OUT Parameters
            return {
                "pRestaurantUserName": out_parameters[0],
                "pStatus": bool(out_parameters[1]),
                "pStatusCheck": out_parameters[2]
            }
        else:
            st.error("Unable to Execute Stored Procedure, Database Connection Failed.")
            return None
    except Error as e:
        st.error(f"Error: {e}")
        return None

    # Streamlit UI
    st.title("MySQL Database Connection and Stored Procedure Testing")
    
    # Execute the Stored Procedure when the Button is Pressed
    if st.button("Call Stored Procedure"):
        stored_procedure_name = "RestaurantSignin"
    
        # Execute the stored procedure
        result = execute_stored_procedure(stored_procedure_name,pRestaurant,pRestaurantUser,pRestaurantUserPassword)

    # Streamlit UI
    st.title("MySQL Database Connection and Stored Procedure Testing")

    # Execute the Stored Procedure when the Button is Pressed / Clicked
    if st.button("Call Stored Procedure"):
        stored_procedure_name = "RestaurantSignin"
    
        # Execute the stored procedure
        result = execute_stored_procedure(stored_procedure_name, pRestaurant, pRestaurantUser, pRestaurantUserPassword,pRestaurantUserName,pStatus,pStatusCheck)
    
        # Display results
        st.write(f"Result: {result}")
        if result:
            st.write(f"pRestaurantUserName: {result['pRestaurantUserName']}")
            st.write(f"pStatus: {result['pStatus']}")
            st.write(f"pStatusCheck: {result['pStatusCheck']}")
        else:
            st.error("Failed to execute stored procedure or retrieve results.")
