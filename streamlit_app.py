import streamlit as st
# from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, APP_NAME, VERSION, CURRENT_USER, IS_AUTHENTICATED, USER_ROLE, ERROR_MESSAGES, SUCCESS_MESSAGES, GUIDELINES
# from db_connection import get_mysql_data
from authentication import render_authentication_ui
from ui_components import render_header, render_data, render_sample_elements
import mysql.connector  # Ensure this import is at the top of your file


# Page Configuration
st.set_page_config(
    page_title="SmartRestaurant",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="auto",
)

# Custom CSS
st.markdown(
    """
    <style>
    body {
        font-family: 'Times New Roman', serif;
        font-size: 8px !important;
    }
    h1 {
        font-family: 'Times New Roman', serif;
        font-size: 14px !important;
        color: #2E86C1 !important;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Titles
# st.title("SmartRestaurant : Sign In Page")
# Body
# st.write("Try signing in here with valid credentials")

# Render the header (example of including modular UI components)
render_header()

# Render the authentication UI
# Render the header
# st.header("SmartRestaurant - Sign In")




def test_db_connection():
    conn = None  # Initialize conn to None before using it
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if conn.is_connected():
            print("Connection successful!")
        else:
            print("Connection failed!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn:
            conn.close()

# Test the database connection
test_db_connection()




# Render authentication UI and get the response
response = render_authentication_ui()

if response:
    if 'error' in response:
        st.error(f"Error: {response['error']}")
        if 'raw_result' in response:
            st.warning(f"Raw result from the stored procedure: {response['raw_result']}")
    else:
        if response.get('pStatus') == 1:
            st.success(f"Welcome, {response['pRestaurantUserName']}!")
            st.info(response['pStatusCheck'])
        else:
            st.warning("Authentication failed.")
            st.info(response['pStatusCheck'])
else:
    st.error("No response received from authentication.")

