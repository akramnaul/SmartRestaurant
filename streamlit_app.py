import streamlit as st
import mysql.connector
from mysql.connector import Error
# from config import *

# Function to Connect remote MySQL Database Server
def connect_database():
    try:
        connection = mysql.connector.connect(
            host=st.secrets["database"]["DB_HOST"],
            user=st.secrets["database"]["DB_USER"],
            password=st.secrets["database"]["DB_PASSWORD"],
            database=st.secrets["database"]["DB_NAME"]
        )
        if connection.is_connected():
            # st.success("Successfully Connected MySQL Database : Rest ! ")
            return connection
        else:
            st.error("Failed to Connect MySQL Database : Rest ! ")
            return None
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to Execute a Stored Procedure
def execute_stored_procedure(stored_procedure_name="RestaurantSignin",pRestaurant="KhanBurger",pRestaurantUser="03004444001",pRestaurantUserPassword="abcd"):
    try:
        connection = connect_database()
        if connection is not None:
            # st.success("Successfully Connected MySQL Database : Rest ! ")
            cursor = connection.cursor()

            # Initialize OUT Parameters for the Stored Procedure RestaurantSignin
            cursor.execute("SET @pRestaurant = 'KhanBurger',@pRestaurantUser = '03004444001',@pRestaurantUserPassword = 'abcd';")

            # Call the Stored Procedure RestaurantSignin
            call_stored_procedure = (
                f"CALL {stored_procedure_name}("
                f"'{pRestaurant}', '{pRestaurantUser}', '{pRestaurantUserPassword}',"    # IN Parameters
                f"@pRestaurantUserName, @pStatus, @pStatusCheck);"                       # OUT Parameters
            )
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

# Stored Procedure User Interface UI
def stored_procedure_ui(): # stored_procedure_name="RestaurantSignin",pRestaurant="KhanBurger",pRestaurantUser="03004444001",pRestaurantUserPassword="abcd"):
    st.title("MySQL Database")
    try:
        connection = connect_database()
        if connection is not None:
            st.success("Successfully Connected DB : Rest ! ")

            # Button to Trigger the Stored Procedure
            if st.button("Click 2 Test : RestaurantSignin"):
                stored_procedure_name = "RestaurantSignin"

                # Declare & Initialize the IN Parameters
                pRestaurant = "KhanBurger"
                pRestaurantUser = "03004444001"
                pRestaurantUserPassword = "abcd"
            
                # Call the Database Stored Procedure
                result = execute_stored_procedure(stored_procedure_name, pRestaurant, pRestaurantUser, pRestaurantUserPassword)
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

stored_procedure_ui() # stored_procedure_name="RestaurantSignin",pRestaurant="KhanBurger",pRestaurantUser="03004444001",pRestaurantUserPassword="abcd")
