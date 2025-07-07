import pandas as pd

def load_data():
    # Replace with your actual data source
    sheet_id = "1IwIjlnjvY2C5kLGN6gKBIp--y2f7MOipyp3e1LcVu1M"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return pd.read_csv(url)

df = load_data()
