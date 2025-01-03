# logic_ui.py
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from database.connect_database import connect_database
from database.stored_procedures import stored_procedures

# Stored Procedure User Interface UI
def stored_procedure_ui():
    st.title("MySQL Database")
    try:
        connection = connect_database()
        if connection is not None:
            st.success("Successfully Connected MySQL Database : Rest ! ")

            # Button to Trigger the Stored Procedure
            if st.button("Click 2 Test : RestaurantSignin"):
                stored_procedure_name = "RestaurantSignin"

                # Declare & Initialize the IN Parameters
                pRestaurant = "KhanBurger"
                pRestaurantUser = "03004444001"
                pRestaurantUserPassword = "abcd"

            # Call the Stored Procedure : Name : IN : OUT Parameters
            stored_procedure_call = (
                f"CALL {stored_procedure_name}("
                f"'{pRestaurant}', '{pRestaurantUser}', '{pRestaurantUserPassword}',"    # IN Parameters
                f"@pRestaurantUserName, @pStatus, @pStatusCheck);"                       # OUT Parameters
            )

            # Call the Database Stored Procedure   : 
                result = execute_stored_procedure(stored_procedure_call) # ,stored_procedure_out_parameters,returning_parameters)
                # Display The Results
                if result:
                    st.write("Stored Procedure OUT Parameters :")
                    # st.write(f"Result : {result}")
                    st.write(f"pRestaurantUserName : {result['pRestaurantUserName']}")
                    st.write(f"pStatus : {result['pStatus']}")
                    st.write(f"pStatusCheck : {result['pStatusCheck']}")
                else:
                    st.error("Failed to execute stored procedure or retrieve results.")
    except Error as e:
        st.error(f"Error: {e}")
        return None
