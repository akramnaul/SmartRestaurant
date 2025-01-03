# stored_procedures.py
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from database.connect_database import connect_database

# Function to Execute a Stored Procedure
def execute_stored_procedure(stored_procedure_call,stored_procedure_out_parameters):
    connection = None
    try:
        # Connect to the database
        connection = connect_database()
        if connection is None:
            st.error("Database Connection Failed. Cannot Execute the Stored Procedure.")
            return None

        # Use a cursor to execute the stored procedure
        with connection.cursor() as cursor:
            cursor.execute(stored_procedure_call)

            # Fetch the OUT parameters
            cursor.execute(stored_procedure_out_parameters)
            returning_out_parameters = cursor.fetchone()

        # Validate and return the result as a dictionary
        if returning_out_parameters:
            return returning_out_parameters
        else:
            st.warning("No Output Parameters Returned from the Stored Procedure.")
            return None

    except Error as e:
        st.exception(f"An Error Occurred While Executing the Stored Procedure: {e}")
        return None

    finally:
        # Ensure the connection is closed
        if connection and connection.is_connected():
            connection.close()
