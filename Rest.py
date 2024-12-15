import streamlit as st
from pathlib import Path
import pandas as pd
from Read import DataLoader  # Assuming this handles CSV loading now
from Pro import DataProcessor

# Constants
FILE_PATH = Path(r"Employee_Activities_June_August_2024.csv")  # Changed to .csv
GRAPH_FOLDER = "graphs"

# Custom CSS for UI styling
st.markdown("""
    <style>
        /* App background */
        .stApp {
            background-color: #151932; /* Dark background */
        }

        /* Headings in bold white */
        h1, h2, h3, h4 {
            color: white; /* White font for headings */
            font-weight: bold;
        }

        /* File loaded message style */
        .stAlert {
            background-color: rgba(139, 139, 139, 0.2); /* Light gray with transparency */
            color: white; /* White font for message text */
            font-weight: bold;
        }

        /* Button styles */
        .stButton > button {
            color: #0C28BB; /* Blue text color */
            background-color: white; /* Button background */
            border-radius: 5px; /* Rounded corners */
            border: none; /* No border */
            font-weight: bold;
        }

        .stButton > button:hover {
            background-color: #0A1E78; /* Darker blue on hover */
            color: white; /* White text on hover */
        }
    </style>
""", unsafe_allow_html=True)


# Title
st.title("Employee Activities Dashboard")
st.write("### Visualize Allotted vs Utilized Hours")

# Helper Function to Render Tables
def render_table_with_custom_style(title, data):
    import pandas as pd
    st.markdown(f"<h4 style='color: black;'>{title}</h4>", unsafe_allow_html=True)
    if isinstance(data, pd.Series):
        data = data.reset_index().rename(columns={0: "Values"})
    st.table(data)

# Load Data
try:
    # Adjust the DataLoader to handle CSV (Assumed DataLoader is updated for CSV)
    loader = DataLoader(FILE_PATH)
    data = loader.load_data()  # This should now load the CSV data
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
