import pandas as pd

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_data(self):
        """
        Load data from the specified CSV file and return a DataFrame.
        """
        try:
            # Check the file extension and load accordingly
            if self.file_path.suffix == '.csv':
                data = pd.read_csv(self.file_path)  # Load CSV file
            else:
                raise ValueError("Unsupported file format. Only CSV files are supported.")
            
            # Convert 'Date' column to datetime
            data['Date'] = pd.to_datetime(data['Date'])
            return data
        except Exception as e:
            raise FileNotFoundError(f"Error loading file: {e}")
