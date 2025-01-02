import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from database.connect_database import *

# Function to Execute a Stored Procedure
def execute_stored_procedure(stored_procedure_call,stored_procedure_out_parameters,returning_parameters):
# def execute_stored_procedure(stored_procedure_name="RestaurantSignin",pRestaurant="KhanBurger",pRestaurantUser="03004444001",pRestaurantUserPassword="abcd"):
    try:
        connection = connect_database()
        if connection is not None:
            # st.success("Successfully Connected MySQL Database : Rest ! ")
            cursor = connection.cursor()

            # # Call the Stored Procedure : Name : IN : OUT Parameters
            # stored_procedure_name_and_in_out_parameters = (
            #     f"CALL {stored_procedure_name}("
            #     f"'{pRestaurant}', '{pRestaurantUser}', '{pRestaurantUserPassword}',"    # IN Parameters
            #     f"@pRestaurantUserName, @pStatus, @pStatusCheck);"                       # OUT Parameters
            # )
            # Call the Stored Procedure RestaurantSignin
            # call_stored_procedure = (stored_procedure_name_and_in_out_parameters)
            #     f"CALL {stored_procedure_name}("
            #     f"'{pRestaurant}', '{pRestaurantUser}', '{pRestaurantUserPassword}',"    # IN Parameters
            #     f"@pRestaurantUserName, @pStatus, @pStatusCheck);"                       # OUT Parameters
            # )

            cursor.execute(stored_procedure_call)

            # Fetch the OUT Parameters from MySQL Server
            # stored_procedure_out_parameters = "SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;"
            cursor.execute(stored_procedure_out_parameters)
            # cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
            out_parameters = cursor.fetchone()

            # Close the Cursor & Database Connection
            cursor.close()
            connection.close()

            # # Return The Results
            # # Store the returning parameters in a variable
            # returning_parameters = {
            #     "pRestaurantUserName": out_parameters[0],
            #     "pStatus": bool(out_parameters[1]),
            #     "pStatusCheck": out_parameters[2],
            # }
            
            # Return the dictionary
            return returning_parameters

            # return {
            #     "pRestaurantUserName": out_parameters[0],
            #     "pStatus": bool(out_parameters[1]),
            #     "pStatusCheck": out_parameters[2],
            # }
        else:
            st.error("Failed to Execute Stored Procedure.....Database Connection Failed.....")
            return None
    except Error as e:
        st.error(f"Error: {e}")
        return None
