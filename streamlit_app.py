import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database configuration
DB_HOST = '192.95.14.153'
DB_USER = 'webbuilderuser'
DB_PASSWORD = 'm7xXGk6scyBv1iPORvmJ'
DB_NAME = 'Rest'

# Function to connect to the database and test stored procedures
def connect_to_db():
    try:
        # Establishing the connection
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

# Function to execute a stored procedure
def execute_stored_procedure(proc_name, params=None):
    try:
        connection = connect_to_db()
        if connection is not None:
            cursor = connection.cursor()
            
            # Call stored procedure
            cursor.callproc(proc_name, params if params else [])
            
            # Fetch and display results from OUT parameters (if any)
            for result in cursor.stored_results():
                st.write("Stored Procedure Result:", result.fetchall())
            
            cursor.close()
            connection.close()
        else:
            st.error("Unable to execute stored procedure, database connection failed.")
    
    except Error as e:
        st.error(f"Error: {e}")

# Streamlit UI
st.title("MySQL Database Connection and Stored Procedure Testing")

# Input for stored procedure name and parameters
proc_name = st.text_input("Enter Stored Procedure Name", "your_procedure_name_here")
params_input = st.text_area("Enter Parameters (comma-separated)", "param1,param2")

# Execute the stored procedure when the button is pressed
if st.button("Test Stored Procedure"):
    params = tuple(map(str, params_input.split(','))) if params_input else None
    execute_stored_procedure(proc_name, params)
