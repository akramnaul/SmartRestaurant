# logic_ui.py
import streamlit as st
from mysql.connector import Error
from dotenv import load_dotenv
import os 
from database.connect_database import connect_database
from database.stored_procedures import execute_stored_procedure

# Load environment variables (if needed for database credentials)
load_dotenv()

# Stored Procedure User Interface
def stored_procedure_ui():
    st.title("MySQL Database Interaction")

    try:
        # Attempt to connect to the database
        connection = connect_database()
        if connection is not None:
            st.success("Successfully connected to the MySQL database!")

            # Button to trigger the stored procedure
            if st.button("Click to Test: RestaurantSignin"):
                # Define stored procedure name and IN parameters
                stored_procedure_name = "RestaurantSignin"
                pRestaurant = "KhanBurger"
                pRestaurantUser = "03004444001"
                pRestaurantUserPassword = "abcd"

                # Build the stored procedure call string
                stored_procedure_call = (
                    f"CALL {stored_procedure_name}("
                    f"'{pRestaurant}', '{pRestaurantUser}', '{pRestaurantUserPassword}',"  # IN Parameters
                    f"@pRestaurantUserName, @pStatus, @pStatusCheck);"                    # OUT Parameters
                )

                # Show loading indicator
                with st.spinner("Executing stored procedure..."):
                    # Execute the stored procedure
                    result = execute_stored_procedure(stored_procedure_call)

                # Display the results
                if result:
                    st.write("Stored Procedure Output Parameters:")
                    st.write(f"pRestaurantUserName: {result['pRestaurantUserName']}")
                    st.write(f"pStatus: {result['pStatus']}")
                    st.write(f"pStatusCheck: {result['pStatusCheck']}")
                else:
                    st.error("Failed to execute the stored procedure or retrieve results.")
        else:
            st.error("Failed to connect to the database. Please check the connection details.")

    except Error as e:
        st.error(f"An error occurred while interacting with the database: {e}")
