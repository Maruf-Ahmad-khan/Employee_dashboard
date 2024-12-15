import streamlit as st
from pathlib import Path
from Read import DataLoader
from Pro import DataProcessor
import openpyxl


# Constants
FILE_PATH = Path("Employee_Activities_June_August_2024.xlsx")
GRAPH_FOLDER = "graphs"

# Debugging: Print the file path
st.write(f"Looking for file at: {FILE_PATH.resolve()}")

# Custom CSS for UI styling
st.markdown("""
    <style>
        .stApp {
            background-color: #800080;
        }
        .dark-black-text {
            color: white;
            font-size: 16px;
            font-weight: bold;
        }
        .stButton > button {
            color: black;
            background-color: #007BFF;
            border-radius: 5px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Employee Activities Dashboard")
st.write("### Visualize Allotted vs Utilized Hours")

# Helper Function to Render Tables
def render_table_with_custom_style(title, data):
    import pandas as pd
    st.markdown(f"<h4 style='color: white;'>{title}</h4>", unsafe_allow_html=True)
    if isinstance(data, pd.Series):
        data = data.reset_index().rename(columns={0: "Values"})
    st.table(data)

# Load Data
try:
    loader = DataLoader(FILE_PATH)
    data = loader.load_data()
    st.success("File loaded successfully!")
except FileNotFoundError as e:
    st.error(f"Error: {e}")
    st.stop()

# Process Data
processor = DataProcessor(data)
results = processor.summarize_data()

# Buttons to Display Outputs
if st.button("Show Summarized Results"):
    render_table_with_custom_style("1. Sum of Allotted Time for Each Employee", results['allotted_sum'])
    render_table_with_custom_style("2. Sum of Allotted Time for Each Employee (Project Wise)", results['allotted_sum_project'])
    render_table_with_custom_style("3. Sum of Utilized Hours for Each Employee", results['utilized_sum'])
    render_table_with_custom_style("4. Sum of Utilized Hours for Each Employee (Project Wise)", results['utilized_sum_project'])

if st.button("Generate and Show Graphs"):
    processor.save_graphs(GRAPH_FOLDER)
    st.write("#### Daily Allotted vs Utilized Hours")
    st.image(f"{GRAPH_FOLDER}/daily_summary.png")

    st.write("#### Weekly Allotted vs Utilized Hours")
    st.image(f"{GRAPH_FOLDER}/weekly_summary.png")

    st.write("#### Monthly Allotted vs Utilized Hours")
    st.image(f"{GRAPH_FOLDER}/monthly_summary.png")
