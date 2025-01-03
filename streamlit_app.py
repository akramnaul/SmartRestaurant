# streamlit_app.py
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os 
from database.connect_database import connect_database
from database.stored_procedures import execute_stored_procedure
from frontend.logic_ui import stored_procedure_ui

stored_procedure_call = (
    f"CALL RestaurantSignin("
    f"'KhanBurger', '03004444001', 'abcd',"            # IN Parameters
    f"@pRestaurantUserName, @pStatus, @pStatusCheck);" # OUT Parameters
)

result = execute_stored_procedure(stored_procedure_call)

    # Display the results
    if result:
        st.write("Stored Procedure Output Parameters:")
        st.write(f"pRestaurantUserName: {result['pRestaurantUserName']}")
        st.write(f"pStatus: {result['pStatus']}")
        st.write(f"pStatusCheck: {result['pStatusCheck']}")
    else:
        st.error("Failed to execute the stored procedure or retrieve results.")

# stored_procedure_ui() # stored_procedure_name="RestaurantSignin",pRestaurant="KhanBurger",pRestaurantUser="03004444001",pRestaurantUserPassword="abcd")
