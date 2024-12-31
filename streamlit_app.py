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
            st.success("Successfully Connected MySQL Database : Rest !")
            return connection
        else:
            st.error("Failed to Connect MySQL Database : Rest !")
            return None
    except Error as e:
        st.error(f"Error : {e} ")
        return None

# Function to Execute Stored Procedure Passing IN and Retrieving OUT Parameters
def execute_stored_procedure(stored_procedure_name, inout_parameters):
    try:
        connection = connect_to_db()
        if connection is not None:
            cursor = connection.cursor()

            # Execute the stored procedure
            call_stored_procedure_query = f"CALL {stored_procedure_name}{inout_parameters};"
            cursor.execute(call_stored_procedure_query)

            # st.write(f"pRestaurantUserName : {inout_parameters[3]}")
            # st.write(f"pStatus : {inout_parameters[4]}")
            # st.write(f"pStatusCheck : {inout_parameters[5]}")

            cursor.close()
            connection.close()
        else:
            st.error("Unable to Execute Stored Procedure, Database Connection Failed.")
    except Error as e:
        st.error(f"Error: {e}")

# Streamlit UI
st.title("MySQL Database Connection and Stored Procedure Testing")

# Execute the Stored Procedure when the Button is Pressed / Clicked
if st.button("Test Stored Procedure"):
    stored_procedure_name = "RestaurantSignin"
    
    parameters = "(pRestaurant,pRestaurantUser,pRestaurantUserPassword,pRestaurantUserName,pStatus,pStatusCheck)"

    execute_stored_procedure(stored_procedure_name, parameters)

    # Fetch the OUT parameter values from the parameter list
    pRestaurantUserName = parameters[3]
    pStatus = parameters[4]
    pStatusCheck = parameters[5]

    st.write("pRestaurantUserName : {pRestaurantUserName}")
    st.write(f"pStatus : {pStatus}")
    st.write(f"pStatusCheck : {pStatusCheck}")
