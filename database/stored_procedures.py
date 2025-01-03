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
            st.error("Database connection failed. Cannot execute the stored procedure.")
            return None

        # Use a cursor to execute the stored procedure
        with connection.cursor() as cursor:
            cursor.execute(stored_procedure_call)

            # Fetch the OUT parameters
            cursor.execute(stored_procedure_out_parameters) # "SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
            out_parameters = cursor.fetchone()

        # Validate and return the result as a dictionary
        if out_parameters:
            return {
                "pRestaurantUserName": out_parameters[0],
                "pStatus": bool(out_parameters[1]),
                "pStatusCheck": out_parameters[2],
            }
        else:
            st.warning("No output parameters returned from the stored procedure.")
            return None

    except Error as e:
        st.exception(f"An error occurred while executing the stored procedure: {e}")
        return None

    finally:
        # Ensure the connection is closed
        if connection and connection.is_connected():
            connection.close()
