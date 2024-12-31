import streamlit as st
import mysql.connector
from mysql.connector import Error

# Function to Connect remote MySQL Database Server
def connect_database():
    try:
        # Database Configuration
        DB_HOST = st.secrets["database"]["DB_HOST"]
        DB_USER = st.secrets["database"]["DB_USER"]
        DB_PASSWORD = st.secrets["database"]["DB_PASSWORD"]
        DB_NAME = st.secrets["database"]["DB_NAME"]

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
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
            st.success("Successfully Connected MySQL Database : Rest ! ")
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
    st.title("MySQL Database Connection and Stored Procedure Testing")
    try:
        connection = connect_database()
        if connection is not None:
            # Button to Trigger the Stored Procedure
            if st.button("Call The Database Stored Procedure : RestaurantSignin"):
                stored_procedure_name = "RestaurantSignin"
                # Declare & Initialize the IN Parameters
                pRestaurant = "KhanBurger"
                pRestaurantUser = "03004444001"
                pRestaurantUserPassword = "abcd"
            
                # Call the Database Stored Procedure
                result = execute_stored_procedure(stored_procedure_name, pRestaurant, pRestaurantUser, pRestaurantUserPassword)
    except Error as e:
        st.error(f"Error: {e}")
        return None
    
    # Display The Results
    if result:
        st.write("Stored Procedure Results:")
        st.write(f"Result : {result}")
        st.write(f"pRestaurantUserName : {result['pRestaurantUserName']}")
        st.write(f"pStatus : {result['pStatus']}")
        st.write(f"pStatusCheck : {result['pStatusCheck']}")
    else:
        st.error("Failed to execute stored procedure or retrieve results.")

stored_procedure_ui(): # stored_procedure_name="RestaurantSignin",pRestaurant="KhanBurger",pRestaurantUser="03004444001",pRestaurantUserPassword="abcd")




# # Database configuration
# DB_HOST = '192.95.14.153'
# DB_USER = 'webbuilderuser'
# DB_PASSWORD = 'm7xXGk6scyBv1iPORvmJ'
# DB_NAME = 'Rest'

# # Function to Connect remote MySQL Database Server
# def connect_to_db():
#     try:
#         connection = mysql.connector.connect(
#             host=DB_HOST,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             database=DB_NAME
#         )
#         if connection.is_connected():
#             st.success("Successfully Connected MySQL Database : Rest ! ")
#             return connection
#         else:
#             st.error("Failed to Connect MySQL Database : Rest ! ")
#             return None
#     except Error as e:
#         st.error(f"Error: {e}")
#         return None

