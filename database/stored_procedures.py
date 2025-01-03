# stored_procedures.py
import streamlit as st
from mysql.connector import Error
from database.connect_database import connect_database

# Function to Execute a Stored Procedure
def execute_stored_procedure(stored_procedure_call):
    connection = None
    try:
        # Connect to the database
        connection = connect_database()
        if connection is None:
            st.error("Database connection failed. Cannot execute the stored procedure.")
            return None

        # Use a cursor to execute the stored procedure
        with connection.cursor() as cursor:
            cursor.execute(stored_procedure_call)

            # Fetch the OUT parameters
            cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
            out_parameters = cursor.fetchone()

        # Return the result as a dictionary
        return {
            "pRestaurantUserName": out_parameters[0],
            "pStatus": bool(out_parameters[1]),
            "pStatusCheck": out_parameters[2],
        }

    except Error as e:
        st.error(f"An error occurred while executing the stored procedure: {e}")
        return None

    finally:
        # Ensure the connection is closed
        if connection is not None and connection.is_connected():
            connection.close()
