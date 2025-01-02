import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from database.connect_database import *

# Function to Execute a Stored Procedure
def execute_stored_procedure(stored_procedure_name="RestaurantSignin",pRestaurant="KhanBurger",pRestaurantUser="03004444001",pRestaurantUserPassword="abcd"):
    try:
        connection = connect_database()
        if connection is not None:
            # st.success("Successfully Connected MySQL Database : Rest ! ")
            cursor = connection.cursor()

            # Initialize OUT Parameters for the Stored Procedure RestaurantSignin
            # cursor.execute("SET @pRestaurant = 'KhanBurger',@pRestaurantUser = '03004444001',@pRestaurantUserPassword = 'abcd';")

            # Call the Stored Procedure RestaurantSignin : Construct Parameters
            stored_procedure_parameters = (
                f"CALL {stored_procedure_name}("
                f"'{pRestaurant}', '{pRestaurantUser}', '{pRestaurantUserPassword}',"    # IN Parameters
                f"@pRestaurantUserName, @pStatus, @pStatusCheck);"                       # OUT Parameters
            )
            # Call the Stored Procedure RestaurantSignin
            call_stored_procedure = (stored_procedure_parameters)
            #     f"CALL {stored_procedure_name}("
            #     f"'{pRestaurant}', '{pRestaurantUser}', '{pRestaurantUserPassword}',"    # IN Parameters
            #     f"@pRestaurantUserName, @pStatus, @pStatusCheck);"                       # OUT Parameters
            # )
            cursor.execute(call_stored_procedure)

            # Fetch the OUT Parameters from MySQL Server
            cursor.execute("SELECT @pRestaurantUserName, @pStatus, @pStatusCheck;")
            out_parameters = cursor.fetchone()

            # Close the Cursor & Database Connection
            cursor.close()
            connection.close()

            # Return The Results
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
