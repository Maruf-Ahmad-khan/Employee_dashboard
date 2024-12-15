import pandas as pd

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_data(self):
        """
        Load data from the specified Excel file and return a DataFrame.
        """
        try:
            data = pd.read_excel(self.file_path)
            data['Date'] = pd.to_datetime(data['Date'])  # Convert 'Date' column to datetime
            return data
        except Exception as e:
            raise FileNotFoundError(f"Error loading file: {e}")
