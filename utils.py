import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path
from dotenv import load_dotenv
import json
import time
load_dotenv()
raw_configs = os.getenv("DATA_CONFIGS", '{}')
data_configs = json.loads(raw_configs)


start = time.time()
def get_data(data_configs:dict=data_configs):
    DATA_DIR = Path(__file__).resolve().parent / 'data'
    data_store = {}
    # csv_paths = list(DATA_DIR.glob('*.csv'))
    
    for filename, row_remove in data_configs.items():
        path = DATA_DIR / f"{filename}.csv"
        if path.exists():
            data_store[filename] = pd.read_csv(path, skiprows=row_remove)
    return data_store
        
class BaseLab:
    def __init__(self, df: pd.DataFrame):
        self._df = df
        
        

    def __getattr__(self, name):
        return getattr(self._df, name)
    
    def __getitem__(self, key):
            # Delegate the bracket lookup to the internal dataframe
            return self._df[key]

    def converter(self, column: str, target_units_in_units: int=1, data_units: int=1):
        df = self._df
        data = self._df[column]
        conversion_factor = data_units / target_units_in_units
        self._df[column] = data * conversion_factor
        return self._df[column]
    
    def graph(self, xaxis: str, yaxis: str, figsize:tuple=(10,10)):
        df = self._df
        

        plt.figure(figsize=figsize)
        plt
        plt.plot(df[xaxis], df[yaxis], label="", color='red')
        plt.title(f"{yaxis.upper().replace("_", " ")} vs {xaxis.upper().replace("_", " ")}")
        plt.xlabel(xaxis.replace("_", " "))
        plt.ylabel(yaxis.replace("_", " "))
        plt.grid(True)          
        plt.legend()
        plt.tight_layout()
        plt.show()
    

    
data_store = get_data()
test = BaseLab(data_store['kinematics'])

# print(test.converter('velocity_mps', 1000))
print(test.graph('distance_m', 'velocity_mps'))






 









