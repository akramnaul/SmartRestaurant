# Database Configuration
DB_HOST = '192.95.14.153'
DB_USER = 'webbuilderuser'
DB_PASSWORD = 'm7xXGk6scyBv1iPORvmJ'
DB_NAME = 'Rest'

# Application Constants
APP_NAME = "Restaurant Management System"
VERSION = "1.0.0"

# Global State (if needed, managed via session state in Streamlit)
CURRENT_USER = None
IS_AUTHENTICATED = False
USER_ROLE = None  # e.g., Admin, Manager, Staff

# Messages
ERROR_MESSAGES = {
    "db_connection": "Unable to connect to the database.",
    "invalid_credentials": "Invalid credentials. Please try again.",
    "missing_fields": "All fields are required.",
}

SUCCESS_MESSAGES = {
    "login_success": "Login successful. Welcome!",
}

# Default Guidelines or Help Texts
GUIDELINES = {
    "register": "If you don't have an account, please contact your administrator.",
    "password_reset": "Forgot your password? Click here to reset.",
}
