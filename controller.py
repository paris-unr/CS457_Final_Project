import os
import pandas as pd

INPUT_PATH = "Cars Datasets 2025.csv"
OUTPUT_PATH = "Carse Datasets 2025 parsed.csv"

def import_csv():
    print("hello world")

    try:
        print("pth to load Kaggle data")
        df = pd.read_csv(INPUT_PATH)

        keep_columns = [ 
            "Company Names",
            "Cars Names",
            "Engines",
            "CC/Battery Capacity",
            "HorsePower",
            "Total Speed",
            "Performance(0 - 100 )KM/H",
            "Cars Prices",
            "Fuel Types",
            "Seats",
            "Torque"
            ]
        
        keep_columns = [c for c in keep_columns if c in df.columns]
        df_clean = df[keep_columns].dropna()
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        df_clean.to_csv(OUTPUT_PATH, index=False)

        return OUTPUT_PATH
    
    except Exception as e:
        print("Failed to Load", e)
        return None
