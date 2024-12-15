import json
import os
import pandas as pd
import streamlit as st

class TaskManager:
    def __init__(self, file_path='task.json'):
        self.file_path = file_path
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from the JSON file."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    tasks = json.load(f)
                    return tasks
            except json.JSONDecodeError:
                return []
        else:
            return []

    def save_tasks(self):
        """Save tasks to the JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, task):
        """Add a new task to the list."""
        self.tasks.append({"task": task, "completed": False})
        self.save_tasks()

    def mark_task_completed(self, task_index):
        """Mark a task as completed."""
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index]['completed'] = True
            self.save_tasks()

    def delete_task(self, task_index):
        """Delete a task from the list."""
        if 0 <= task_index < len(self.tasks):
            self.tasks.pop(task_index)
            self.save_tasks()

    def to_dataframe(self):
        """Convert tasks to a Pandas DataFrame."""
        return pd.DataFrame(self.tasks)

# Styling
st.markdown("""
    <style>
        .stApp {
            background-color: #151932; /* Dark background */
        }
        h1, h2, h3, h4, h5, h6, p, label {
            color: white;
        }
        .stButton > button {
            color: #0C28BB; /* Blue text color */
            background-color: white; /* Button background */
            border-radius: 5px; /* Rounded corners */
            border: none; /* No border */
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #0A1E78; /* Darker blue on hover */
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# App
st.title("Task Manager")
st.write("### Manage your tasks efficiently!")

manager = TaskManager()

# Add Task
task = st.text_input("Enter a new task:")
if st.button("Add Task"):
    if task.strip():
        manager.add_task(task)
        st.success("Task added successfully!")
    else:
        st.error("Task cannot be empty!")

# Display Tasks
st.write("### Task List:")
if manager.tasks:
    for i, task in enumerate(manager.tasks):
        col1, col2, col3 = st.columns([6, 2, 2])
        with col1:
            st.write(f"{i + 1}. {task['task']} - {'Completed' if task['completed'] else 'Pending'}")
        with col2:
            if not task['completed'] and st.button(f"Mark Completed {i}", key=f"complete_{i}"):
                manager.mark_task_completed(i)
                st.experimental_rerun()
        with col3:
            if st.button(f"Delete {i}", key=f"delete_{i}"):
                manager.delete_task(i)
                st.experimental_rerun()
else:
    st.write("No tasks available.")

# Raw JSON View
if st.checkbox("View Raw JSON Data"):
    st.json(manager.tasks)

import io  # Add this import for BytesIO

# Download Options
st.write("### Download Data")
task_df = manager.to_dataframe()

col_csv, col_excel, col_json = st.columns(3)
with col_csv:
    csv = task_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download as CSV", csv, "tasks.csv", "text/csv")

with col_excel:
    # Use BytesIO as a buffer for Excel data
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        task_df.to_excel(writer, index=False)
    excel_buffer.seek(0)  # Rewind the buffer
    st.download_button(
        label="Download as Excel",
        data=excel_buffer,
        file_name="tasks.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col_json:
    json_data = json.dumps(manager.tasks, indent=4)
    st.download_button("Download as JSON", json_data, "tasks.json", "application/json")
