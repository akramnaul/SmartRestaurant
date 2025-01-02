import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Function to Connect remote MySQL Database Server
def connect_database():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
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
