import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_mysql_data():
    """
    Connects to the MySQL database and fetches tables and procedures.
    Returns:
        tuple: (list of tables, list of procedures)
    """
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
        return [], f"Error: {err}"
