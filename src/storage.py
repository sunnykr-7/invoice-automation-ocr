import pandas as pd
import os

def save_to_excel(data, file_path):
    df_new = pd.DataFrame([data])

    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            df_existing = pd.read_excel(file_path, engine="openpyxl")
            df_final = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_final = df_new
    except Exception as e:
        print("Excel Read Error:", e)
        df_final = df_new

    df_final.to_excel(file_path, index=False, engine="openpyxl")