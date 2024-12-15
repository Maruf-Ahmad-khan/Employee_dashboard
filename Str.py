import streamlit as st
import plotly.express as px
import pandas as pd
import io
from Task import TaskManager  # Ensure TaskManager is correctly imported

# Initialize TaskManager
manager = TaskManager()

# Custom CSS for the app
st.markdown("""
    <style>
        .stApp {
            background-color: #151932;
        }
        h1, h2, h3, h4 {
            color: white;
            font-weight: bold;
        }
        .stButton > button {
            color: #0C28BB;
            background-color: white;
            border-radius: 5px;
            border: none;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #0A1E78;
            color: white;
        }
        .css-1fcdlhm {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for refresh
if "refresh" not in st.session_state:
    st.session_state.refresh = False

# App Title
st.title("Task Manager")

# Input Section
st.write("### Add a Task")
date = st.date_input("Select Date:")
time = st.time_input("Select Time:")
subject = st.selectbox("Select Subject:", [
    "Python", "SQL", "Excel", "Power BI", "Machine Learning",
    "Generative AI", "ML Ops", "Git and GitHub", "Linux",
    "Statistics", "Maths"
])

if st.button("Add Task"):
    manager.add_task(str(date), str(time), subject)
    st.success("Task added successfully!")
    # Trigger refresh
    st.session_state.refresh = True

# Display Tasks
st.write("### Task List")
tasks_df = manager.to_dataframe()
if tasks_df.empty:
    st.info("No tasks available.")
else:
    # Display the tasks in a DataFrame format
    st.dataframe(tasks_df)

    # Add delete functionality for each task
    for i, task in tasks_df.iterrows():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        # Safely access keys with .get()
        col1.write(task.get('Date', 'N/A'))
        col2.write(task.get('Subject', 'N/A'))
        
        # Button to delete task
        if col3.button(f"Delete Task {i}"):
            manager.delete_task(i)
            # Trigger refresh
            st.session_state.refresh = True

# Performance Analysis
st.write("### Performance Analysis")
if not tasks_df.empty:
    analysis = manager.performance_analysis()

    # Line Graph: Sub vs Date
    st.write("#### Line Graph: Subjects Over Dates")
    line_date_fig = px.line(
        analysis["line_date"], x='Date', y='Count', color='Subject',
        title="Subjects vs Date"
    )
    st.plotly_chart(line_date_fig, use_container_width=True)

    # Line Graph: Sub vs Time
    st.write("#### Line Graph: Subjects Over Time")
    line_time_fig = px.line(
        analysis["line_time"], x='Time', y='Count', color='Subject',
        title="Subjects vs Time"
    )
    st.plotly_chart(line_time_fig, use_container_width=True)

    # Pie Chart: Time Spent on Subjects
    st.write("#### Pie Chart: Time Spent on Subjects")
    pie_chart_fig = px.pie(
        analysis["pie_chart"], names=analysis["pie_chart"].index,
        values=analysis["pie_chart"].values, title="Time Spent on Subjects"
    )
    st.plotly_chart(pie_chart_fig, use_container_width=True)

# Download Section
st.write("### Download Data")
col_csv, col_excel, col_json = st.columns(3)

with col_csv:
    csv = tasks_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "tasks.csv", "text/csv")

with col_excel:
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        tasks_df.to_excel(writer, index=False)
    excel_buffer.seek(0)
    st.download_button(
        "Download Excel", excel_buffer, "tasks.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col_json:
    json_data = tasks_df.to_json(orient="records", indent=4)
    st.download_button("Download JSON", json_data, "tasks.json", "application/json")

# Perform Refresh Logic
if st.session_state.refresh:
    # Reset the refresh flag and rerun the app
    st.session_state.refresh = False
    st.experimental_rerun()
