import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database configuration
DB_HOST = '192.95.14.153'
DB_USER = 'webbuilderuser'
DB_PASSWORD = 'm7xXGk6scyBv1iPORvmJ'
DB_NAME = 'Rest'

# Function to connect to the database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            st.success("Successfully connected to the database!")
            return connection
        else:
            st.error("Failed to connect to the database.")
            return None
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to execute a stored procedure and handle OUT parameters
def execute_stored_procedure(proc_name, in_params, out_param_count):
    try:
        connection = connect_to_db()
        if connection is not None:
            cursor = connection.cursor()

            # Prepare parameters (IN and OUT)
            params = list(in_params) + [None] * out_param_count
            
            # Call the stored procedure
            cursor.callproc(proc_name, params)

            # Fetch results
            st.write("Stored Procedure Execution Results:")
            for result in cursor.stored_results():
                st.write(result.fetchall())

            # Fetch OUT parameters
            st.write("OUT Parameters:")
            for i in range(len(in_params), len(params)):
                st.write(f"OUT Param {i - len(in_params) + 1}: {params[i]}")

            cursor.close()
            connection.close()
        else:
            st.error("Unable to execute stored procedure, database connection failed.")
    except Error as e:
        st.error(f"Error: {e}")

# Streamlit UI
st.title("MySQL Database Connection and Stored Procedure Testing")

# Input for stored procedure name
proc_name = st.text_input("Enter Stored Procedure Name", "your_procedure_name_here")

# Input for IN parameters
in_params_input = st.text_area("Enter IN Parameters (comma-separated)", "param1,param2")
in_params = tuple(map(str.strip, in_params_input.split(','))) if in_params_input else ()

# Input for number of OUT parameters
out_param_count = st.number_input("Enter Number of OUT Parameters", min_value=0, step=1, value=0)

# Execute the stored procedure when the button is pressed
if st.button("Test Stored Procedure"):
    execute_stored_procedure(proc_name, in_params, out_param_count)
