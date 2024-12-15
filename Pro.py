import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px


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
    
    def generate_daily_graph(self):
        """
        Generate a dynamic daily summary graph using Plotly.
        """
        daily_summary = self.data.groupby('Date').agg({'Allotted Hours': 'sum', 'Utilized Hours': 'sum'}).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily_summary['Date'], y=daily_summary['Allotted Hours'], 
                                 mode='lines+markers', name='Allotted Hours'))
        fig.add_trace(go.Scatter(x=daily_summary['Date'], y=daily_summary['Utilized Hours'], 
                                 mode='lines+markers', name='Utilized Hours'))
        fig.update_layout(
            title="Daily Allotted vs Utilized Hours",
            xaxis_title="Date",
            yaxis_title="Hours",
            template="plotly_dark"
        )
        return fig

    def generate_weekly_graph(self):
        """
        Generate a dynamic weekly summary graph using Plotly.
        """
        self.data['Week'] = self.data['Date'].dt.isocalendar().week
        weekly_summary = self.data.groupby('Week').agg({'Allotted Hours': 'sum', 'Utilized Hours': 'sum'}).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=weekly_summary['Week'], y=weekly_summary['Allotted Hours'], name='Allotted Hours'))
        fig.add_trace(go.Bar(x=weekly_summary['Week'], y=weekly_summary['Utilized Hours'], name='Utilized Hours'))
        fig.update_layout(
            title="Weekly Allotted vs Utilized Hours",
            xaxis_title="Week",
            yaxis_title="Hours",
            barmode="group",
            template="plotly_dark"
        )
        return fig

    def generate_monthly_graph(self):
        """
        Generate a dynamic monthly summary graph using Plotly.
        """
        self.data['Month'] = self.data['Date'].dt.month
        monthly_summary = self.data.groupby('Month').agg({'Allotted Hours': 'sum', 'Utilized Hours': 'sum'}).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=monthly_summary['Month'], y=monthly_summary['Allotted Hours'], name='Allotted Hours'))
        fig.add_trace(go.Bar(x=monthly_summary['Month'], y=monthly_summary['Utilized Hours'], name='Utilized Hours'))
        fig.update_layout(
            title="Monthly Allotted vs Utilized Hours",
            xaxis_title="Month",
            yaxis_title="Hours",
            barmode="group",
            template="plotly_dark"
        )
        return fig
