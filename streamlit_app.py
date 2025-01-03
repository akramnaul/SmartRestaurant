# streamlit_app.py
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os 
from database.connect_database import connect_database
from database.stored_procedures import execute_stored_procedure
from frontend.logic_ui import stored_procedure_ui

stored_procedure_ui() # stored_procedure_name="RestaurantSignin",pRestaurant="KhanBurger",pRestaurantUser="03004444001",pRestaurantUserPassword="abcd")
