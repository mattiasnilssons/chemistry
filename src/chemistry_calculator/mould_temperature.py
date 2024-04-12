import pandas as pd
import os

def get_mould_data():
    print("Current working directory:", os.getcwd())
    df = pd.read_excel('/Users/Mattias/Workspaces/personal/chemistry/src/chemistry_calculator/temp_rh_time.xlsx', header=1)
    df['Unit'] = pd.to_datetime(df['Unit'])
    df['dates'] = df['Unit']
    df["temperatures"] = df['°C']
    df["humidity"] = df['%RH']
    return df
