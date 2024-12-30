import streamlit as st

def render_header():
    """Render the main header of the Streamlit app."""
    st.header("SmartRestaurant Header")
    st.title("Signin")
    # st.write("Hello StreamlitPage!")

def render_data(tables, procedures):
    """
    Render tables and procedures in the UI.
    Args:
        tables (list): List of database tables.
        procedures (list): List of stored procedures.
    """
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

def render_sample_elements():
    """Render other sample Streamlit elements."""
    st.subheader('This is a subheader')
    st.markdown('_Markdown_')
    st.text('This is sample text')
    st.latex(r''' e^{i\pi} + 1 = 10 ''')
    st.caption('This is a caption')
