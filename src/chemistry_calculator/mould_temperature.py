import pandas as pd
import os

def get_mould_data():
    print("Current working directory:", os.getcwd())
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    pathname = os.path.join(BASE_DIR, 'temp_rh_time.json')
    df = pd.read_json(pathname)
    if df['Unit'].dtype is 'int64':
        df['Unit'] = pd.to_datetime(df['Unit'], unit='s')
    else:
        df['Unit'] = pd.to_datetime(df['Unit'], errors='coerce')  # Coerce errors to handle unparsable formats

    df['dates'] = df['Unit']
    df["temperatures"] = df['°C']
    df["humidity"] = df['%RH']
    df["water_content"] = df['g/m3']
    print(f"datafame: {df.head(5)}")
    return df


