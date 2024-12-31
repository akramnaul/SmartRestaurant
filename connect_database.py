import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database configuration
DB_HOST = st.secrets["database"]["DB_HOST"]
DB_USER = st.secrets["database"]["DB_USER"]
DB_PASSWORD = st.secrets["database"]["DB_PASSWORD"]
DB_NAME = st.secrets["database"]["DB_NAME"]

# DB_HOST = '192.95.14.153'
# DB_USER = 'webbuilderuser'
# DB_PASSWORD = 'm7xXGk6scyBv1iPORvmJ'
# DB_NAME = 'Rest'

# Function to Connect remote MySQL Database Server
def connect_mysql_database():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            st.success("Successfully Connected MySQL Database : Rest ! ")
            return connection
        else:
            st.error("Failed to Connect MySQL Database : Rest ! ")
            return None
    except Error as e:
        st.error(f"Error: {e}")
        return None
