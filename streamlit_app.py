import streamlit as st
import mysql.connector

# Remote MySQL connection credentials
DB_HOST = '192.95.14.153'
DB_USER = 'webbuilderuser'
DB_PASSWORD = 'm7xXGk6scyBv1iPORvmJ'
DB_NAME = 'Rest'

# Function to connect to MySQL database and fetch tables and procedures
def get_mysql_data():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Query to fetch tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        # Query to fetch stored procedures
        cursor.execute("SHOW PROCEDURE STATUS WHERE Db = %s", (DB_NAME,))
        procedures = cursor.fetchall()

        cursor.close()
        conn.close()

        return tables, procedures

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return [], []

# Streamlit UI
st.header("StreamlitPage Header" + ": My Header")
st.title("StreamlitPage Title")
st.write("Hello StreamlitPage!")

# Display Tables and Procedures
tables, procedures = get_mysql_data()

st.subheader('Tables in the Database:')
if tables:
    for table in tables:
        st.write(f"- {table[0]}")
else:
    st.write("No tables found.")

st.subheader('Stored Procedures in the Database:')
if procedures:
    for procedure in procedures:
        st.write(f"- {procedure[1]}")  # Procedure name is in the second column
else:
    st.write("No stored procedures found.")

# Display other Streamlit elements
st.subheader('This is a subheader')
st.markdown('_Markdown_')
st.text('This is sample text')
st.latex(r''' e^{i\pi} + 1 = 10 ''')
st.caption('This is a caption')

# rest of your UI code (checkbox, radio buttons, etc.)
