import json
import os
import pandas as pd
from datetime import datetime

class TaskManager:
    def __init__(self, file_path='task.json'):
        self.file_path = file_path
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from the JSON file."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    print("Loaded tasks:", data)  # Debugging: Check loaded tasks
                    return data
            except json.JSONDecodeError:
                print("Error: Corrupted JSON file.")
                return []
        return []

    def save_tasks(self):
        """Save tasks to the JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, date, time, subject):
        """Add a new task to the task list."""
        if not date or not time or not subject:
            print("Invalid task details")  # Debugging: Ensure all fields are provided
            return
        self.tasks.append({"Date": date, "Time": time, "Subject": subject})
        self.save_tasks()

    def delete_task(self, index):
        """Delete a task by its index."""
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks()

    def to_dataframe(self):
        """Convert tasks to a Pandas DataFrame."""
        if not self.tasks:
            return pd.DataFrame(columns=["Date", "Time", "Subject"])  # Initialize with columns
        df = pd.DataFrame(self.tasks)
        required_columns = ["Date", "Time", "Subject"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = None  # Add missing columns with default None values
        return df

    def performance_analysis(self):
        """
        Generate data for performance analysis:
        - Line Graph: Sub vs Date
        - Line Graph: Sub vs Time
        - Pie Chart: Time spent on each subject.
        """
        df = self.to_dataframe()
        if df.empty or "Date" not in df.columns or "Time" not in df.columns:
            return {
                "line_date": pd.DataFrame(),
                "line_time": pd.DataFrame(),
                "pie_chart": pd.Series(dtype=int)
            }
        
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
        df = df.dropna(subset=['Datetime'])  # Drop rows with invalid dates

        # Pie Chart: Time spent per subject
        time_spent = df['Subject'].value_counts()

        return {
            "line_date": df.groupby(['Date', 'Subject']).size().reset_index(name='Count'),
            "line_time": df.groupby(['Time', 'Subject']).size().reset_index(name='Count'),
            "pie_chart": time_spent
        }
