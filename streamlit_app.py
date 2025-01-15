# Check the streamlit code
# streamlit_app.py
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os 
from database.connect_database import connect_database
from database.execute_stored_procedure import execute_stored_procedure
from frontend.restaurant_landing_page import signin

signin()

