# stored_procedures.py

import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from database.connect_database import connect_database

# Function to Execute a Stored Procedure
def execute_stored_procedure(stored_procedure_call):
    try:
        connection = connect_database()
        if connection is not None:
            # st.success("Successfully Connected MySQL Database : Rest ! ")
            cursor = connection.cursor()
            cursor.execute(stored_procedure_call)

            # Fetch the OUT Parameters from MySQL Server
            # stored_procedure_out_parameters = "SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;"
            cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
            out_parameters = cursor.fetchone()

            # Close the Cursor & Database Connection
            cursor.close()
            connection.close()

            return {
                "pRestaurantUserName": out_parameters[0],
                "pStatus": bool(out_parameters[1]),
                "pStatusCheck": out_parameters[2],
            }
        else:
            st.error("Failed to Execute Stored Procedure.....Database Connection Failed.....")
            return None
    except Error as e:
        st.error(f"Error: {e}")
        return None
