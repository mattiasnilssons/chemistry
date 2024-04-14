import pandas as pd
import os

def get_mould_data():
    print("Current working directory:", os.getcwd())
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    pathname = os.path.join(BASE_DIR, 'temp_rh_time.xlsx')
    print("Pathname:", pathname)
    df = pd.read_excel(pathname, header=1)
    df['Unit'] = pd.to_datetime(df['Unit'])
    df['dates'] = df['Unit']
    df["temperatures"] = df['°C']
    df["humidity"] = df['%RH']
    print(f"Excel file: {df.head(5)}")
    return df
