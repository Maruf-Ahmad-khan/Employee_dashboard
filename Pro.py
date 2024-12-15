import pandas as pd
import matplotlib.pyplot as plt
import os

class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def summarize_data(self):
        """
        Summarize the data for allotted and utilized hours.
        Returns results as a dictionary of Pandas DataFrames/Series.
        """
        results = {}
        # 1. Sum of Allotted Time for Each Employee
        results['allotted_sum'] = self.data.groupby('Employee Name')['Allotted Hours'].sum()
        
        # 2. Sum of Allotted Time for Each Employee (Project Wise)
        results['allotted_sum_project'] = self.data.groupby(['Employee Name', 'Activity'])['Allotted Hours'].sum()
        
        # 3. Sum of Utilized Hours for Each Employee
        results['utilized_sum'] = self.data.groupby('Employee Name')['Utilized Hours'].sum()
        
        # 4. Sum of Utilized Hours for Each Employee (Project Wise)
        results['utilized_sum_project'] = self.data.groupby(['Employee Name', 'Activity'])['Utilized Hours'].sum()
        
        return results
    
    def save_graphs(self, folder_path):
        """
        Generate and save daily, weekly, and monthly visual graphs as images.
        """
        # Create output folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Add 'Week' and 'Month' columns
        self.data['Week'] = self.data['Date'].dt.isocalendar().week
        self.data['Month'] = self.data['Date'].dt.month
        
        # Daily Summary
        daily_summary = self.data.groupby('Date').agg({'Allotted Hours': 'sum', 'Utilized Hours': 'sum'})
        plt.figure(figsize=(8, 5))
        plt.plot(daily_summary.index, daily_summary['Allotted Hours'], label='Allotted Hours', marker='o')
        plt.plot(daily_summary.index, daily_summary['Utilized Hours'], label='Utilized Hours', marker='x')
        plt.title("Daily Allotted vs Utilized Hours")
        plt.xlabel("Date")
        plt.ylabel("Hours")
        plt.legend()
        plt.grid()
        plt.savefig(f"{folder_path}/daily_summary.png")
        plt.close()

        # Weekly Summary
        weekly_summary = self.data.groupby('Week').agg({'Allotted Hours': 'sum', 'Utilized Hours': 'sum'})
        plt.figure(figsize=(8, 5))
        plt.plot(weekly_summary.index, weekly_summary['Allotted Hours'], label='Allotted Hours', marker='o')
        plt.plot(weekly_summary.index, weekly_summary['Utilized Hours'], label='Utilized Hours', marker='x')
        plt.title("Weekly Allotted vs Utilized Hours")
        plt.xlabel("Week")
        plt.ylabel("Hours")
        plt.legend()
        plt.grid()
        plt.savefig(f"{folder_path}/weekly_summary.png")
        plt.close()

        # Monthly Summary
        monthly_summary = self.data.groupby('Month').agg({'Allotted Hours': 'sum', 'Utilized Hours': 'sum'})
        plt.figure(figsize=(8, 5))
        plt.bar(monthly_summary.index - 0.2, monthly_summary['Allotted Hours'], width=0.4, label='Allotted Hours')
        plt.bar(monthly_summary.index + 0.2, monthly_summary['Utilized Hours'], width=0.4, label='Utilized Hours')
        plt.title("Monthly Allotted vs Utilized Hours")
        plt.xlabel("Month")
        plt.ylabel("Hours")
        plt.legend()
        plt.grid()
        plt.savefig(f"{folder_path}/monthly_summary.png")
        plt.close()
