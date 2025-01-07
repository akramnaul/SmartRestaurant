# Check the streamlit code
# streamlit_app.py
# import streamlit as st
# import mysql.connector
# from mysql.connector import Error
# from dotenv import load_dotenv
# import os 
# from database.connect_database import connect_database
# from database.stored_procedures import execute_stored_procedure
# from frontend.restaurant_landing_page import signin

# signin()
# stored_procedure_ui() # stored_procedure_name="RestaurantSignin",pRestaurant="KhanBurger",pRestaurantUser="03004444001",pRestaurantUserPassword="abcd")

import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

# Set the page configuration
st.set_page_config(
    page_title="Streamlit Graphics Demo",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("Streamlit Graphics Demo")
st.write("Explore the power of Streamlit to create interactive graphics and visualizations in the browser!")

# Sidebar options
st.sidebar.header("Settings")
chart_type = st.sidebar.selectbox("Choose a chart type:", ["Line Chart", "Bar Chart", "Scatter Plot"])
animation_enabled = st.sidebar.checkbox("Enable Animation", value=True)

# Generate random data
data = pd.DataFrame(
    np.random.randn(50, 3),
    columns=["Feature 1", "Feature 2", "Feature 3"]
)

# Display the selected chart type
st.subheader(f"{chart_type} Example")
if chart_type == "Line Chart":
    st.line_chart(data)
elif chart_type == "Bar Chart":
    st.bar_chart(data)
else:
    st.write("Scatter Plot Example:")
    fig, ax = plt.subplots()
    ax.scatter(data["Feature 1"], data["Feature 2"], c=data["Feature 3"], cmap='viridis', alpha=0.7)
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    st.pyplot(fig)

# Animation section
if animation_enabled:
    st.subheader("Real-time Animation")
    placeholder = st.empty()
    for i in range(100):
        animated_data = pd.DataFrame(
            np.random.randn(50, 2),
            columns=["X", "Y"]
        )
        with placeholder.container():
            st.line_chart(animated_data)
        time.sleep(0.1)

# User interaction example
st.subheader("Interactive Widgets")
selected_feature = st.selectbox("Select a feature to highlight:", data.columns)
highlight_threshold = st.slider("Set the highlight threshold:", min_value=-3.0, max_value=3.0, value=0.0)

# Highlight selected rows
highlighted_data = data[data[selected_feature] > highlight_threshold]
st.write(f"Rows where **{selected_feature} > {highlight_threshold}:**", highlighted_data)

# Footer
st.write("---")
st.write("Built with ❤️ using [Streamlit](https://streamlit.io/).")
