import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database configuration
DB_HOST = '192.95.14.153'
DB_USER = 'webbuilderuser'
DB_PASSWORD = 'm7xXGk6scyBv1iPORvmJ'
DB_NAME = 'Rest'

# Function to connect to MySQL database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            st.success("Successfully connected to MySQL Database: Rest!")
            return connection
        else:
            st.error("Failed to connect to MySQL Database: Rest!")
            return None
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to execute a stored procedure
def execute_stored_procedure(
    stored_procedure_name="RestaurantSignin",
    pRestaurant="KhanBurger",
    pRestaurantUser="03004444001",
    pRestaurantUserPassword="abcd"
):
    try:
        connection = connect_to_db()
        if connection is not None:
            cursor = connection.cursor()

            # Initialize OUT parameters
            cursor.execute("SET @pRestaurantUserName = '';")
            cursor.execute("SET @pStatus = FALSE;")
            cursor.execute("SET @pStatusCheck = '';")

            # Call the stored procedure
            call_query = (
                f"CALL {stored_procedure_name}("
                f"'{pRestaurant}', '{pRestaurantUser}', '{pRestaurantUserPassword}', "
                f"@pRestaurantUserName, @pStatus, @pStatusCheck);"
            )
            cursor.execute(call_query)

            # Fetch the OUT parameters
            cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
            out_parameters = cursor.fetchone()

            # Close the connection
            cursor.close()
            connection.close()

            # Return the results
            return {
                "pRestaurantUserName": out_parameters[0],
                "pStatus": bool(out_parameters[1]),
                "pStatusCheck": out_parameters[2],
            }
        else:
            st.error("Failed to execute stored procedure. Database connection failed.")
            return None
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Streamlit UI
st.title("MySQL Database Connection and Stored Procedure Testing")

# Button to trigger stored procedure
if st.button("Call Stored Procedure"):
    stored_procedure_name = "RestaurantSignin"

    # Input parameters
    pRestaurant = "KhanBurger"
    pRestaurantUser = "03004444001"
    pRestaurantUserPassword = "abcd"

    # Call the stored procedure
    result = execute_stored_procedure(
        stored_procedure_name, pRestaurant, pRestaurantUser, pRestaurantUserPassword
    )

    # Display the results
    if result:
        st.write("Stored Procedure Results:")
        st.write(f"pRestaurantUserName: {result['pRestaurantUserName']}")
        st.write(f"pStatus: {result['pStatus']}")
        st.write(f"pStatusCheck: {result['pStatusCheck']}")
    else:
        st.error("Failed to execute stored procedure or retrieve results.")
